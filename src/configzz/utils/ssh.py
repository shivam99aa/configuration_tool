import paramiko
import logging

from configzz.utils.exceptions import InvalidSSHCommand


class SSH:

    """

    SSH class to maintain ssh connections to servers and run commands.

    """

    def __init__(self, fqdn: str = None, username: str = None, password: str = None, key: str = None):

        """

        Init method to create SSH object.

        :param fqdn: FQDN of remote server.
        :type fqdn: str
        :param username: Username to login in remote server.
        :type username: str
        :param password: Password to login in remote server.
        :type password: str
        :param key: Key to login in remote server.
        :type key: str

        """

        self.logger = logging.getLogger(__name__)

        self.fqdn = fqdn
        self.username = username
        self.password = password
        self.key = key

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self) -> bool:

        """

        Method to create connection to remote server.

        :return: Boolean telling if connection is made or not.
        :rtype: bool

        """

        try:
            if self.password is not None:
                self.ssh_client.connect(hostname=self.fqdn, username=self.username, password=self.password)
            else:
                self.ssh_client.connect(hostname=self.fqdn, username=self.username, key_filename=self.key)
            self.logger.debug(f'SSH connection made to {self.fqdn}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to create SSH connection to {self.fqdn}')
            self.logger.error(f'{e}')
            return False

    def execute_command(self, command: str):

        """

        Method to execute command on remote server.

        :param command: Command to be executed on remote server.
        :type command: str
        :return: stdout and stderr lists
        :rtype: lists

        """

        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)

            stdout = stdout.readlines()
            stderr = stderr.readlines()

        except Exception as e:
            raise InvalidSSHCommand(e)

        return stdout, stderr

    def copy_file(self, src_file, dest_file):

        """

        Method to copy file from local machine to remote machine.

        :param src_file: File on local machine.
        :type src_file: str
        :param dest_file: File path on remote machine.
        :type dest_file: str

        """

        try:
            ftp_client = self.ssh_client.open_sftp()
            ftp_client.put(src_file, dest_file)
            self.logger.info(f"Copied file {src_file} to {dest_file} on {self.fqdn}")
            ftp_client.close()
        except Exception as e:
            raise InvalidSSHCommand(e)
        finally:
            ftp_client.close()

    def close(self):
        self.ssh_client.close()
