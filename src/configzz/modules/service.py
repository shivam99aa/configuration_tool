import logging

from configzz.utils.ssh import SSH
from configzz.utils.exceptions import InvalidTaskConfiguration


class Service:

    """

    Service class to perform tasks related to service on servers.

    """

    def __init__(self, ssh_client: SSH):

        """

        Init method to create Service object.

        :param ssh_client: ssh_client to connect to servers
        :type ssh_client: SSH object

        """

        self.logger = logging.getLogger(__name__)
        self.ssh_client = ssh_client

    def _get_service_state(self, service_name: str) -> str:

        """

        Method to get state of the service on server.

        :param service_name: Name of the service for which
        :type service_name: str
        :return: State of the service
        :rtype: str

        """

        command = f'service {service_name} status'
        stdout, stderr = self.ssh_client.execute_command(command)
        if f'Unit {service_name}.service could not be found' in ''.join(stderr):
            return 'absent'
        elif 'active (running)' in ''.join(stdout):
            return 'running'
        elif 'inactive (dead)' in ''.join(stdout):
            return 'stopped'
        else:
            return "error"

    def _start_service(self, service_name: str) -> bool:

        """

        Method to start a service on server.

        :param service_name: Name of service to be started.
        :type service_name: str
        :return: Boolean telling if service is started or not.
        :rtype: bool

        """

        command = f'service {service_name} start'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stderr:
            return False
        else:
            return True

    def _stop_service(self, service_name: str) -> bool:

        """

        Method to stop the service on server.

        :param service_name: Name of service to be stopped.
        :type service_name: str
        :return: Boolean telling if service is topped or not
        :rtype: bool

        """

        command = f'service {service_name} stop'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stderr:
            return False
        else:
            return True

    def _restart_service(self, service_name: str) -> bool:

        """

        Method to restart service on server.

        :param service_name: Name of service to be restarted.
        :type service_name: str
        :return: Boolean telling if service is restarted or not.
        :rtype: bool

        """

        command = f'service {service_name} restart'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stderr:
            return False
        else:
            return True

    def handler(self, service_config: dict):

        """

        Handler to manage all service related operations on server.

        :param service_config: Dictionary containing all service related configurations.
        :type service_config: dict

        """

        if service_config.get('state') not in ['stopped', 'running', 'restarted']:
            raise InvalidTaskConfiguration("Service state can be stopped, running or restarted only.")

        service_state = self._get_service_state(service_config.get('name'))

        if service_state == 'absent':
            self.logger.error(f"Invalid service name {service_config.get('name')}")
        elif service_state == 'running' and service_config.get('state') == 'stopped':
            if not self._stop_service(service_config.get('name')):
                self.logger.error(f"Unable to stop service {service_config.get('name')}")
            else:
                self.logger.info(f"Stopped service {service_config.get('name')}")
        elif service_state == 'stopped' and service_config.get('state') == 'running':
            if not self._start_service(service_config.get('name')):
                self.logger.error(f"Unable to start service {service_config.get('name')}")
            else:
                self.logger.info(f"Started service {service_config.get('name')}")
        elif service_config['state'] == 'restarted':
            if not self._restart_service(service_config.get('name')):
                self.logger.error(f"Unable to restart service {service_config.get('name')}")
            else:
                self.logger.info(f"Restarted service {service_config.get('name')}")
        else:
            self.logger.info(f"service {service_config.get('name')} is already {service_config.get('state')}")
