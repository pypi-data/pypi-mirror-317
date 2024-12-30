import json
import os
import time
from threading import Thread
from airosentris.algorithm.BERT.BERTRunner import BERTRunner
from airosentris.client.APIClient import APIClient
from airosentris.logger.Logger import Logger
from airosentris.message.TestParams import TestParams
from airosentris.config.ConfigFetcher import get_config
from airosentris import get_agent
from airosentris.client.RabbitMQClient import RabbitMQClient
from minio import Minio
import tempfile

from airosentris.runner.RunnerFactory import RunnerFactory


class Tester:
    def __init__(self):        
        self.rabbitmq_client = None
        self.test_queue = "airosentris.test.queue"
        self.test_thread = None
        self.runners = {}
        self.runner_cache = {}
        self.api_client = APIClient()
        self.logger = Logger(__name__)

    def setup_rabbitmq_client(self):
        """Initialize RabbitMQ client."""
        config = get_config()
        self.rabbitmq_client = RabbitMQClient(config=config)
        self.rabbitmq_client.connect()
        self.logger.info("RabbitMQ client initialized successfully.")

    def initialize_test_queue(self):
        """Declare the test queue."""
        if not self.rabbitmq_client:
            self.setup_rabbitmq_client()
        self.rabbitmq_client.declare_queue(self.test_queue, durable=True)
        self.logger.info(f"Evaluation queue initialized: {self.test_queue}")

    def start_listening(self):
        """Listen to incoming messages for test."""
        while True:
            try:
                self.initialize_test_queue()
                self.rabbitmq_client.consume_messages(
                    self.test_queue,
                    self._process_incoming_message,
                )
                self.logger.info(f"[*] Waiting for messages in {self.test_queue}. To exit press CTRL+C")
            except Exception as e:
                self.logger.error(f"Error in start_listening: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)

    def _process_incoming_message(self, ch, method, properties, body):
        """Process incoming RabbitMQ message."""
        try:
            message_data = json.loads(body)
            message = TestParams(
                project_id=message_data.get("project_id"),
                run_id=message_data.get("run_id"),
                algorithm=message_data.get("algorithm"),
                scope=message_data.get("scope"),
                content=message_data.get("content"),
            )
            self.process_test_message(message)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON message: {e}")
            if not ch.is_closed:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                self.logger.warning("Cannot ack message; channel is already closed.") 
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            if not ch.is_closed:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                self.logger.warning("Cannot ack message; channel is already closed.") 

    def process_test_message(self, message: TestParams):
        run_id = message.run_id
        algorithm = message.algorithm
        scope = message.scope
        if run_id and (scope not in self.runner_cache or self.runner_cache[scope] != run_id):            
            runner_class = RunnerFactory.get_runner(algorithm)
            runner_instance = runner_class()
            model_path = runner_instance.download_model(run_id)
            runner_instance.load_model(scope, model_path)
            self.runners[scope] = runner_instance
            self.runner_cache[scope] = run_id
        runner = self.runners.get(scope)
        if not runner:
            self.logger.warning(f"No runner found for scope: {scope}")
            return
        result = runner.evaluate(message)

    def start_message_listener(self):
        """Start a thread for test listener."""
        Thread(target=self.start_listening, daemon=True).start()

    def start(self):
        """Start all runner processes."""
        self.start_message_listener()
