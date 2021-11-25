from home_ai.Task import Task


class HelloWorld(Task):
    def __init__(self, *args, **kwargs):
        super().__init__("home_ai__hello_world", *args, **kwargs)

    def run(self, *args):
        self.output("Hello World")

