import yaml
import logging

from configzz.utils.exceptions import InvalidYAMLfile


class Inventory:

    """

    Inventory class to parse inventory file and return hosts configuration.

    """

    def __init__(self):

        """

        Init method creates inventory object.

        """

        self.logger = logging.getLogger(__name__)

    def read_inventory_file(self, inventory_file: str) -> dict:

        """

        Read inventory yaml file and return dict.

        :param inventory_file: Inventory file containing hosts and their configuration.
        :type inventory_file: str
        :return: dictionary containing hosts configuration.
        :rtype: dict

        """

        try:
            return yaml.load(open(inventory_file).read(), yaml.SafeLoader)
        except yaml.YAMLError as e:
            raise InvalidYAMLfile(e)
