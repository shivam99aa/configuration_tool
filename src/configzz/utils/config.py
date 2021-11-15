import yaml
import logging

from configzz.utils.defaults import Defaults
from configzz.utils.exceptions import InvalidYAMLfile


class Config:

    """

    Config class to parse config file and return configuration.

    """

    def __init__(self, defaults: Defaults = None):

        """

        Init method creates defaults config and create Config object.


        :param defaults: default config present in Defaults class
        :type defaults: Defaults

        """

        self.logger = logging.getLogger(__name__)
        self.cfg = {
            'log_level': defaults.log_level,
            'ssh': defaults.ssh
        }

    def read_config(self, config_file: str = None) -> dict:

        """
        This method reads config file and merge it with default config overriding default values with user provided one.

        :param config_file: yaml config file.
        :type config_file: str
        :return: dictionary of configurations.
        :rtype: dict

        """

        try:
            config = yaml.load(open(config_file).read(), yaml.SafeLoader)

            # Only INFO, WARNING, DEBUG and ERROR log levels are supported.
            if config['log_level'] not in ['INFO', 'WARNING', 'DEBUG', 'ERROR']:
                self.logger.warning(f"log_level {config['log_level']} is invalid. "
                                    f"Using default log level.")
                config['log_level'] = self.cfg.get('log_level')

            return {**self.cfg, **config}

        except yaml.YAMLError as e:
            raise InvalidYAMLfile(e)
