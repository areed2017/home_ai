import json
import os


class HAConfig:
    def __init__(self):
        self.interface = "cli"
        self.task_path = '~/home_ai'
        self.packages = []
        self.default = {}
        self.hello_world = {}

        if not os.path.exists('.ai_config'):
            self.setup_config()
        else:
            config_raw = open('.ai_config')
            config = json.load(config_raw)
            for attr in config.keys():
                setattr(self, attr, config[attr])

    def add_attribute(self, app_name, key, default_value=None):
        if key not in (obj := getattr(self, app_name)):
            obj[key] = default_value() if callable(default_value) else default_value
            self.save()

    def get_attribute(self, app_name, key):
        if key in (obj := getattr(self, app_name)):
            return obj[key]
        return None

    def set_attribute(self, app_name, key, value=None):
        if key in (obj := getattr(self, app_name)):
            obj[key] = value
            self.save()
        else:
            self.add_attribute(app_name, key, value)

    def add_package(self, package_name):
        self.packages.append(package_name)
        setattr(self, package_name, dict())
        self.save()

    def remove_package(self, package_name):
        self.packages.remove(package_name)
        delattr(self, package_name)
        self.save()

    def save(self):
        with open(".ai_config", 'w') as file:
            file.write(
                json.dumps(
                    self.__dict__,
                    indent=4,
                    sort_keys=True
                )
            )

    def setup_config(self):
        print("Welcome to Home AI!")
        print("Before starting answer some of these configuration questions...")
        print()
        print("How would you like to comunicate with your AI?")
        print("1. Command Line")
        print("2. Talking")
        interface_in = input("> ")

        print()
        print("How would you like your AI to talk to you?")
        print("1. Command Line")
        print("2. Talking")
        interface_out = input("> ")

        if interface_in == "1" and interface_out == "1":
            self.interface = "cli"
        elif interface_in == "1" and interface_out == "2":
            self.interface = "cli_in_tts_out"
        else:
            print("This is not developed yet...")
            quit()

        print()
        print("Where would you like to store raw task files?")
        self.task_path = input("> ")
        self.task_path = self.task_path[:-1] if self.task_path.endswith("/") else self.task_path
        self.save()
        os.system("python main.py --install default")
        os.system("python main.py --install hello_world")
