import logging
import argparse
import sys

from configzz.utils.defaults import Defaults
from configzz.utils.ssh import SSH
from configzz.utils.config import Config
from configzz.utils.inventory import Inventory
from configzz.modules.controller import Controller

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_file_presence():
    pass


def main():
    parser = argparse.ArgumentParser(description="Process configzz arguments", add_help=False)

    parser.add_argument('tasks', nargs=1, help='tasks to execute on servers.')

    parser.add_argument('--help', '-h', action='help', help='Show help.')
    parser.add_argument('--config_file', '-c', help='config file for tool.')
    parser.add_argument('--inventory', '-i', required=True, help='inventory file containing server list.')

    args = parser.parse_args()

    ##TODO: ###
    # Check if all the files passed in arguments exist or not?
    # write a validator method for inventory schema

    config = Config(args.config_file, Defaults())
    logger.info(f'{config.cfg}')
    logger.setLevel(level=config.cfg['log_level'])

    inventory = Inventory(args.inventory)
    task_list = Controller().read_tasks(args.tasks[0])
    logger.warning(task_list)
    ssh_client = SSH()
    module_objects = Controller.module_object_generator(ssh_client)

    try:
        for host in inventory.hosts_config:
            logger.info(host)

            if 'ssh' not in host and config.cfg['ssh'] is None:
                logger.warning(f"No ssh setting found. Skipping host {host['name']}.")
                continue
            elif 'ssh' not in host:
                host['ssh'] = config.cfg['ssh']

            ssh_client.fqdn = host['fqdn']
            ssh_client.username = host['ssh']['username']
            if 'password' in host['ssh']:
                ssh_client.password = host['ssh']['password']
            elif 'key' in host['ssh']:
                ssh_client.key = host['ssh']['key']
            else:
                logger.error(f'No creds found. Skipping host {host["name"]}')
                continue

            if not(ssh_client.connect()):
                continue

            for task_dict in task_list:
                for task in task_dict:
                    logger.info(f'Running task {task}')
                    module_objects[task].handler(task_dict[task])

            ssh_client.close()
    except Exception as e:
        logger.error(f'Error occurred when configuring hosts. {e}')
        sys.exit(1)

