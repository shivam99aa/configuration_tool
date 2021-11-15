import yaml
import logging

from configzz.utils.ssh import SSH
from configzz.utils.exceptions import InvalidYAMLfile
from configzz.modules.package import Package
from configzz.modules.file import File
from configzz.modules.service import Service


class Controller:

    """

    Controller class to deal with modules.

    """

    def __init__(self):

        """

        Initialize controller object.

        """

        self.logger = logging.getLogger(__name__)

    def read_tasks(self, task_file: str) -> list:

        """

        Read tasks yaml file and return dict containing tasks.

        :param task_file: yaml file containing list of tasks to be executed on servers.
        :type task_file: str
        :return: list of dicts containing tasks.
        :rtype: list

        """

        try:
            return yaml.load(open(task_file).read(), yaml.SafeLoader)
        except yaml.YAMLError as e:
            raise InvalidYAMLfile(e)

    @staticmethod
    def module_object_generator(ssh_client: SSH) -> dict:

        """

        Static method to generate a dictionary of module objects.

        :param ssh_client: ssh client which will be used to execute tasks on servers.
        :type ssh_client: SSH object
        :return: dict of module objects.
        :rtype: dict

        """

        return {
            'package': Package(ssh_client),
            'service': Service(ssh_client),
            'file': File(ssh_client)
        }
