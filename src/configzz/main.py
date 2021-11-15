import logging
import argparse
import sys
import os

from configzz.utils.defaults import Defaults
from configzz.utils.ssh import SSH
from configzz.utils.config import Config
from configzz.utils.inventory import Inventory
from configzz.utils.exceptions import InvalidYAMLfile, InvalidTaskConfiguration, InvalidSSHCommand
from configzz.modules.controller import Controller

logger = logging.getLogger()
configuration = Config(Defaults())
# setting log level to Default  which will be changed later based on config provided by user.
logger.setLevel(configuration.cfg.get('log_level'))
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_file_presence(file_name: str) -> bool:

    """

    This method checks if a file exists at given path in system or not.

    :param file_name: Name of file to be checked.
    :type file_name: str
    :rtype: bool

    """

    return os.path.exists(file_name)


def main():

    """

    Main method which start the program and executes configuration tool steps.

    """

    parser = argparse.ArgumentParser(description="Process configzz arguments", add_help=False)

    parser.add_argument('tasks', nargs=1, help='tasks to execute on servers.')

    parser.add_argument('--help', '-h', action='help', help='Show help.')
    parser.add_argument('--config_file', '-c', help='config file for tool.')
    parser.add_argument('--inventory', '-i', required=True, help='inventory file containing server list.')

    args = parser.parse_args()

    # Check if files passed in arguments exist on system or not before proceeding.
    if args.config_file is not None and not check_file_presence(args.config_file):
        logger.error(f"Config file {args.config_file} does not exist")
        sys.exit(1)

    if not check_file_presence(args.inventory):
        logger.error(f"Inventory file {args.inventory} does not exist.")
        sys.exit(1)

    if not check_file_presence(args.tasks[0]):
        logger.error(f"Tasks file {args.tasks[0]} does not exist.")
        sys.exit(1)

    # reading yaml files passed in argument.
    try:
        if args.config_file is not None:
            config = configuration.read_config(args.config_file)
            logger.setLevel(level=config.get('log_level'))
        else:
            config = configuration.cfg

        logger.debug(f'{config}')

    except InvalidYAMLfile as e:
        logger.error(f"Invalid configuration file.\nError:{e}")
        sys.exit(1)

    try:
        inventory = Inventory().read_inventory_file(args.inventory)
        logger.debug(inventory)
    except InvalidYAMLfile as e:
        logger.error(f"Invalid inventory file.\nError:{e}")
        sys.exit(1)

    try:
        task_list = Controller().read_tasks(args.tasks[0])
        logger.debug(task_list)
    except InvalidYAMLfile as e:
        logger.error(f"Invalid tasks file.\nError:{e}")
        sys.exit(1)

    ssh_client = SSH()
    # Generate dict containing objects for each module.
    module_objects = Controller.module_object_generator(ssh_client)

    for host in inventory:
        try:
            logger.info(f"Configuring host: {host['name']}")

            # ssh credentials must be passed either in config as common credentials or in inventory for each host.
            if 'ssh' not in host and config.get('ssh') is None:
                logger.warning(f"No ssh setting found. Skipping host {host['name']}.")
                continue
            elif 'ssh' not in host:
                host['ssh'] = config.get('ssh')

            ssh_client.fqdn = host.get('fqdn')
            ssh_client.username = host.get('ssh').get('username')
            if 'password' in host.get('ssh'):
                ssh_client.password = host.get('ssh').get('password')
            elif 'key' in host.get('ssh'):
                ssh_client.key = host.get('ssh').get('key')
            else:
                logger.error(f'No credentials found. Skipping host {host["name"]}')
                continue

            if not(ssh_client.connect()):
                continue

            for task_dict in task_list:
                for task in task_dict:
                    logger.debug(f'Running task {task}')
                    module_objects[task].handler(task_dict[task])

            ssh_client.close()
        except InvalidTaskConfiguration as e:
            logger.error(f'Error occurred when running task {task}.\nError: {e}\nSkipping current host.')
            continue
        except InvalidSSHCommand as e:
            logger.error(f'Error occurred executing SSH actions.\nError: {e}')
        except Exception as e:
            logger.error(f'Error occurred when configuring hosts. {e}')
            sys.exit(1)
