from threading import Thread

from home_ai.Task import _OUTPUT


class TaskInterface:
    is_running: bool = True
    _THREADS = []

    def __setitem__(self, key, value):
        if hasattr(self, key):
            raise Exception(f"Duplicate Tasks by the name of {key}")
        setattr(self, key, value)

    def run(self):
        handler_thread = Thread(target=self._output_handler)
        handler_thread.start()
        TaskInterface._THREADS.append(handler_thread)
        try:
            self._handler()
        except KeyboardInterrupt:
            self.handle_output("Good bye!")
            self.close()

    def get_input(self):
        pass

    def handle_output(self, output):
        pass

    @staticmethod
    def is_talking():
        return len(_OUTPUT) > 0

    def run_task(self, taskname, *args, **kwargs):
        if hasattr(self, taskname):
            task = getattr(self, taskname)
            task.run(*args, **kwargs)
        else:
            self.handle_output(f"Unknown task {taskname}")

    def run_task_threaded(self, task_name, *args, **kwargs):
        if hasattr(self, task_name):
            task = getattr(self, task_name)
            task.run(*args, **kwargs)
            thread = Thread(target=task.run, args=args, kwargs=kwargs)
            TaskInterface._THREADS.append(thread)
            thread.start()
        else:
            self.handle_output(f"Unknown task {task_name}")

    def close(self):
        self.is_running = False

    def _handler(self):
        while self.is_running:
            self.get_input()
        for thread in TaskInterface._THREADS:
            thread.join()

    def _output_handler(self):
        while self.is_running:
            if len(_OUTPUT) > 0:
                self.handle_output(_OUTPUT.pop())
