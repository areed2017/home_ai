from home_ai.Task import Task


class Default(Task):
    def __init__(self, *args, **kwargs):
        super().__init__("default", *args, **kwargs)

    def run(self, *args):
        self.output(*args)

