import yaml
import logging
from configzz.utils.defaults import Defaults
import sys


class Config:
    """
    Config class to parse config file and return configurations.
    """

    def __init__(self, config_file: str = None, defaults: Defaults = None):
        self.logger = logging.getLogger(__name__)
        self.cfg = {
            'log_level': defaults.log_level,
            'ssh': defaults.ssh
        }

        if config_file is not None:
            try:
                config = yaml.load(open(config_file).read(), yaml.SafeLoader)

                if config['log_level'] not in ['INFO', 'WARNING', 'DEBUG', 'ERROR']:
                    self.logger.warning(f"log_level {config['log_level']} is invalid. "
                                        f"Using default log level.")
                    config['log_level'] = defaults.log_level
                self.cfg = {**self.cfg, **config}
            except yaml.YAMLError as e:
                self.logger.error(f'Error reading config file: {config_file}.')
                self.logger.error(f'Error: {e}')
                sys.exit(1)
