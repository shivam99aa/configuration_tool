import yaml
import logging
import sys


class Inventory:
    """
    Inventory class to parse inventory file and return hosts.
    """

    def __init__(self, inventory_file: str):
        self.logger = logging.getLogger(__name__)
        try:
            self.hosts_config = yaml.load(open(inventory_file).read(), yaml.SafeLoader)
        except yaml.YAMLError as e:
            self.logger.error(f'Error reading inventory file: {inventory_file}.')
            self.logger.error(f'Error: {e}')
            sys.exit(1)

    def _inventory_validator(self):
        pass
