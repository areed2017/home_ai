from Config import HAConfig

# Could cause issues in async
_OUTPUT = []


class Task:
    def __init__(self, task_name: str, config: HAConfig):
        self._task_name = task_name
        self.config = config

    def run(self, *args, **kwargs):
        """To be implemented by extention"""
        pass

    @staticmethod
    def output(*args):
        _OUTPUT.extend(args)

    def use_state(self, key: str, default_value=None):
        def set_value(_value):
            return self.config.set_attribute(self._task_name, key, _value)

        set_value(default_value)
        value = self.config.get_attribute(app_name=self._task_name, key=key)
        return value, set_value
