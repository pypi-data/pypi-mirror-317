class TestParams:
    def __init__(self, project_id, run_id, algorithm, scope, content):
        self.project_id = project_id,
        self.run_id = run_id,
        self.algorithm = algorithm
        self.scope = scope
        self.content = content
    def __repr__(self):
        return f"TestParams(project_id={self.project_id}, run_id={self.run_id}, algorithm={self.algorithm}, " \
               f"scope={self.scope}, content={self.content})"