import time
from home_ai.TaskInterface import TaskInterface
import pyttsx3


class CLIToTTS(TaskInterface):

    def get_input(self):
        while self.is_talking():
            pass
        time.sleep(0.00001)

        user_input = input("USER >> ")
        if user_input in ["quit", 'quit()', 'exit']:
            self.close()

        if user_input.startswith('run '):
            user_input_data = user_input[4:].split(" ")
            task, task_args = user_input_data[0], user_input_data[1:]

            if hasattr(self, task):
                getattr(self, task)(*task_args)
            else:
                self.handle_output("Unknown command.")
        else:
            getattr(self, "default")(user_input)

    def handle_output(self, output):
        text_speak = pyttsx3.init()
        text_speak.say(output)
        text_speak.runAndWait()


def get_interface():
    return CLIToTTS()
