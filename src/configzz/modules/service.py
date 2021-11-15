import logging


class Service:

    def __init__(self, ssh_client):
        self.logger = logging.getLogger(__name__)
        self.ssh_client = ssh_client

    def _get_service_state(self, service_name: str) -> str:
        command = f'service {service_name} status'
        stdout, stderr = self.ssh_client.execute_command(command)
        if f'Unit {service_name}.service could not be found' in ''.join(stderr):
            self.logger.error(f'Invalid service name {service_name}.')
            return 'absent'
        elif 'active (running)' in ''.join(stdout):
            self.logger.info(f'service is running.')
            return 'running'
        elif 'inactive (dead)' in ''.join(stdout):
            self.logger.info(f'service is stopped.')
            return 'stopped'
        else:
            return "error"

    def _start_service(self, service_name: str) -> bool:
        command = f'service {service_name} start'
        stdout, stderr = self.ssh_client.execute_command(command)
        return True

    def _stop_service(self, service_name: str) -> bool:
        command = f'service {service_name} stop'
        stdout, stderr = self.ssh_client.execute_command(command)
        return True

    def _restart_service(self, service_name: str) -> bool:
        command = f'service {service_name} restart'
        stdout, stderr = self.ssh_client.execute_command(command)
        return True

    def handler(self, service_config: dict):
        self.logger.info(service_config)
        service_state = self._get_service_state(service_config['name'])
        if service_state == 'absent':
            self.logger.error(f'Invalid service name {service_config["name"]}')
        elif service_state == 'running' and service_config['state'] == 'stopped':
            self._stop_service(service_config['name'])
        elif service_state == 'stopped' and service_config['state'] == 'running':
            self._start_service(service_config['name'])
        elif service_config['state'] == 'restarted':
            self._restart_service(service_config["name"])
        else:
            self.logger.info(f'service {service_config["name"]} is already {service_config["state"]}')
