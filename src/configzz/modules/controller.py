import yaml
import logging
import sys

from configzz.modules.package import Package
from configzz.modules.file import File
from configzz.modules.service import Service


class Controller:
    """
    Controller class to deal with modules.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_tasks(self, task_file: str) -> dict:
        try:
            return yaml.load(open(task_file).read(), yaml.SafeLoader)
        except yaml.YAMLError as e:
            self.logger.error(f'Error reading story file: {task_file}.')
            self.logger.error(f'Error: {e}')
            sys.exit(1)

    @staticmethod
    def module_object_generator(ssh_client) -> dict:
        return {
            'package': Package(ssh_client),
            'service': Service(ssh_client),
            'file': File(ssh_client)
        }