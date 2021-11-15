import paramiko
import logging
import sys


class SSH:
    """
    SSH class to maintain ssh connections to servers and run commands.
    """

    def __init__(self, fqdn: str = None, username: str = None, password: str = None, key: str = None):
        print(__name__)
        self.logger = logging.getLogger(__name__)

        self.fqdn = fqdn
        self.username = username
        self.password = password
        self.key = key

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self) -> bool:
        try:
            if self.password is not None:
                self.ssh_client.connect(hostname=self.fqdn, username=self.username, password=self.password)
            else:
                self.ssh_client.connect(hostname=self.fqdn, username=self.username, key_filename=self.key)
            self.logger.info(f'SSH connection made to {self.fqdn}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to create SSH connection to {self.fqdn}')
            self.logger.error(f'{e}')
            return False

    def execute_command(self, command: str):
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)

            stdout = stdout.readlines()
            stderr = stderr.readlines()

        except Exception as e:
            self.logger.error(f"Failed to run command {command} due to error: {e}")
            sys.exit(1)

        return stdout, stderr

    def copy_file(self, src_file, dest_file):
        try:
            ftp_client = self.ssh_client.open_sftp()
            ftp_client.put(src_file, dest_file)
            ftp_client.close()
        except Exception as e:
            self.logger.error(f'Failed to copy {src_file} to {dest_file} due to error {e}')
            sys.exit(1)
        finally:
            ftp_client.close()

    def close(self):
        self.ssh_client.close()