import logging
import sys


class Package:

    def __init__(self, ssh_client):
        self.logger = logging.getLogger(__name__)
        self.ssh_client = ssh_client

    def _check_package(self, package_name: str) -> bool:
        command = f"dpkg-query -W -f='${{Status}}' {package_name} | grep -c 'ok installed'"
        stdout, stderr = self.ssh_client.execute_command(command)

        if stdout[0].rstrip() == '1':
            return True
        else:
            return False

    def _install_package(self, package) -> bool:
        command = f'export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get -yq install {package}'
        stdout, stderr = self.ssh_client.execute_command(command)

        # self.logger.info(stdout)
        # self.logger.info(stderr)

        return True

    def _remove_package(self, package):
        command = f'export DEBIAN_FRONTEND=noninteractive && apt-get -yq remove {package}'

        stdout, stderr = self.ssh_client.execute_command(command)

        # self.logger.info(stdout)
        # self.logger.info(stderr)

        return True

    def handler(self, package_config: dict):
        if package_config['state'] not in ['present', 'absent']:
            self.logger.error('State can be either present or absent.')
            sys.exit(1)
        for package in package_config['name']:
            self.logger.info(f'installing {package}')
            if self._check_package(package) and package_config['state'] == 'absent':
                self._remove_package(package)
            elif not self._check_package(package) and package_config['state'] == 'present':
                self._install_package(package)
            else:
                self.logger.info(f'Package {package} already {package_config["state"]}')

