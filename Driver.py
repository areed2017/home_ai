import importlib
import inspect
import os.path
import shutil
import sys
from io import BytesIO
from zipfile import ZipFile

import requests

from Config import HAConfig
from logging import getLogger

from home_ai.Task import Task

LOGGER = getLogger("Home AI")


class Driver:
    def __init__(self):
        self.config = HAConfig()
        self.interface = self.load_interface()
        self.load_packages()

    def install(self, package_name):
        data = requests.get(f"http://127.0.0.1:5000/install/{package_name}")
        if data.status_code != 404:
            file = BytesIO(data.content)
            with ZipFile(file) as files:
                files.extractall(self.config.task_path)

    def uninstall(self, package_name):
        shutil.rmtree(os.path.join(self.config.task_path, package_name))
        self.config.remove_package(package_name)

    def create(self, package_name: str):

        obj_name = "".join([name.capitalize() for name in package_name.split("_")])
        from_path = os.path.join(self.config.task_path, 'default')
        to_path = os.path.join(self.config.task_path, package_name)
        print(self.config.task_path)
        print(from_path)
        print(to_path)
        shutil.copytree(from_path, to_path)

        with open(os.path.join(to_path, f"{package_name}/__init__.py"), 'r') as file:
            file_data = file.read()
        with open(os.path.join(to_path, f"{package_name}/__init__.py"), 'w') as file:
            file_data = file_data.replace("Default", obj_name)
            file_data = file_data.replace("default", package_name)
            file.write(file_data)

        self.config.add_package(package_name)
        print(f"Task created at {to_path}")

    def run(self):
        self.interface.run()

    def load_interface(self):
        _interface = self.config.interface
        LOGGER.info(f"loading Interface ({_interface})...")
        interface_module = importlib.import_module(f"home_ai.interfaces.{_interface}")
        if hasattr(interface_module, 'get_interface'):
            interface = interface_module.get_interface()
        else:
            LOGGER.error(f"Interface ({_interface}) missing 'get_interface' function...")
            raise Exception("Interface missing 'get_interface' function")
        return interface

    def load_packages(self):
        LOGGER.info("Importing packages...")
        for task in self.config.packages:
            sys.path.insert(1, self.config.task_path)
            module = importlib.import_module(f'tasks.{task}')
            LOGGER.info(f"Importing {task}...")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name == "Task" or isinstance(obj, Task):
                    continue
                # noinspection PyProtectedMember
                setattr(self.interface, obj(self.config)._task_name, obj(self.config).run)
                break
