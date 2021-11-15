import logging

from configzz.utils.ssh import SSH
from configzz.utils.exceptions import InvalidTaskConfiguration


class Package:

    """

    Package class to perform package related operations on server.

    """

    def __init__(self, ssh_client: SSH):

        """

        Init method to return Package class object.

        :param ssh_client: ssh client which will be used to perform package related operations on servers.
        :type ssh_client: SSH object

        """

        self.logger = logging.getLogger(__name__)
        self.ssh_client = ssh_client

    def _check_package(self, package_name: str) -> bool:

        """

        Method to check if a package is already installed on server or not.

        :param package_name: Name of the package to check.
        :type package_name: str
        :return: Boolean telling if package is present or not.
        :rtype: bool

        """

        command = f"dpkg-query -W -f='${{Status}}' {package_name} | grep -c 'ok installed'"
        stdout, stderr = self.ssh_client.execute_command(command)

        self.logger.debug(f"stdout to check package {package_name}: {stdout}")
        self.logger.debug(f"stderr to check package {package_name}: {stderr}")

        if stdout[0].rstrip() == '1':
            return True
        else:
            return False

    def _install_package(self, package_name: str) -> bool:

        """

        Method to install package on remote server.

        :param package_name: Name of package to be installed.
        :type package_name: str
        :return: Boolean telling if package is installed or not.
        :rtype: bool

        """

        command = f'export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get -yq install {package_name}'
        stdout, stderr = self.ssh_client.execute_command(command)

        self.logger.debug(f"stdout to install package {package_name}: {stdout}")
        self.logger.debug(f"stderr to install package {package_name}: {stderr}")

        if stderr:
            return False
        else:
            return True

    def _remove_package(self, package_name: str):

        """

        Method to remove package on remote server.

        :param package_name: Name of package to be removed.
        :type package_name:  str
        :return: Boolean telling if package is removed or not.
        :rtype: bool

        """

        command = f'export DEBIAN_FRONTEND=noninteractive && apt-get -yq remove {package_name}'

        stdout, stderr = self.ssh_client.execute_command(command)

        self.logger.debug(f"stdout to remove package {package_name}: {stdout}")
        self.logger.debug(f"stderr to remove package {package_name}: {stderr}")

        if stderr:
            return False
        else:
            return True

    def handler(self, package_config: dict):

        """
        Handler method to handle all package related tasks.

        :param package_config: Dictionary containing package related configuration.
        :type package_config: dict

        """

        if package_config.get('state') not in ['present', 'absent']:
            raise InvalidTaskConfiguration("Package state can be present or absent only.")

        for package in package_config.get('name'):
            self.logger.debug(f'Installing {package}')
            if self._check_package(package) and package_config.get('state') == 'absent':
                if not self._remove_package(package):
                    self.logger.error(f"Unable to remove package {package}")
                else:
                    self.logger.info(f"Removed package {package}")
            elif not self._check_package(package) and package_config.get('state') == 'present':
                if not self._install_package(package):
                    self.logger.error(f"Unable to install package {package}")
                else:
                    self.logger.info(f"Installed package {package}")
            else:
                self.logger.info(f"Package {package} already {package_config.get('state')}")
