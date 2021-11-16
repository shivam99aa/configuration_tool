import logging
import os

from configzz.utils.ssh import SSH
from configzz.utils.exceptions import InvalidTaskConfiguration


class File:

    """

    File class to perform file related operations on server.

    """

    def __init__(self, ssh_client: SSH):

        """

        Init method to create file object.

        :param ssh_client: ssh client which will be used to perform file related operations on servers.
        :type ssh_client: SSH object

        """

        self.logger = logging.getLogger(__name__)
        self.ssh_client = ssh_client

    def _check_dest_file_exists(self, file_path: str) -> bool:

        """

        Method to check if a file exists on remote server.

        :param file_path: Path of file on remote server.
        :type file_path: str
        :return: Boolean telling if file path exists or not.
        :rtype: bool

        """

        command = f'if [[ -f "{file_path}" ]]; then echo "file exists"; else echo "file missing"; fi'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stdout[0].rstrip() == "file exists":
            return True
        elif stdout[0].rstrip() == "file missing":
            return False
        else:
            self.logger.error("Got unexpected output")
            return False

    def _check_src_file_exists(self, file_path: str) -> bool:

        """

        Method to check if a file exists on local machine.

        :param file_path: Path of file on local machine.
        :type file_path: str
        :return: Boolean telling if file exists or not.
        :rtype: bool

        """

        if os.path.exists(file_path):
            return True
        else:
            return False

    def _update_owner(self, file_path: str, owner: str) -> bool:

        """

        Method to update owner of a file on remote server.

        :param file_path: Path of file on remote server.
        :type file_path: str
        :param owner: Owner of the file on remote server.
        :type owner: str
        :return: Boolean telling if owner is updated or not.
        :rtype: bool

        """

        command = f'chown {owner}: {file_path}'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stderr:
            return False
        else:
            return True

    def _update_group(self, file_path: str, group: str) -> bool:

        """

        Method to update group of a file on remote server.

        :param file_path: Path of file on remote server.
        :type file_path: str
        :param group: Group of the file on remote server.
        :type group: str
        :return: Boolean telling if group is updated or not.
        :rtype: bool

        """

        command = f'chgrp {group} {file_path}'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stderr:
            return False
        else:
            return True

    def _update_mode(self, file_path: str, mode: str) -> bool:

        """

        Method to update mode of file on remote server.

        :param file_path: Path of file on remote server.
        :type file_path: str
        :param mode: Mode of the file on remote server.
        :type mode: str
        :return: Boolean telling if mode is updated or not.
        :rtype: bool

        """

        command = f'chmod {mode} {file_path}'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stderr:
            return False
        else:
            return True

    def _remove_file(self, file_path: str) -> bool:

        """

        Method to remove file on remote server.
        :param file_path: Path of file on remote server.
        :type file_path: str
        :return: Boolean telling if file is removed or not.
        :rtype: bool

        """

        command = f"rm {file_path}"
        stdout, stderr = self.ssh_client.execute_command(command)

        if stderr:
            return False
        else:
            return True

    def _copy_file(self, src_file: str, dest_file: str):

        """

        Method to copy file from local machine to remote server.

        :param src_file: Path of file on local machine.
        :type src_file: str
        :param dest_file: Path of file on remote server.
        :type dest_file: str

        """

        self.ssh_client.copy_file(src_file, dest_file)

    def handler(self, file_config: dict):

        """

        Handler method to handle all file related operations.

        :param file_config: Dictionary containing file related configurations.
        :type file_config: dict

        """

        if file_config.get('state') not in ['present', 'absent']:
            raise InvalidTaskConfiguration("File state can be present or absent only.")

        if 'dest' not in file_config:
            raise InvalidTaskConfiguration("Destination file is missing.")

        if file_config.get('state') == 'absent':
            if not self._check_dest_file_exists(file_config.get('dest')):
                self.logger.info(f"{file_config.get('dest')} already absent")
            else:
                if not self._remove_file(file_config.get('dest')):
                    self.logger.error(f"Unable to remove file {file_config.get('dest')}")
                else:
                    self.logger.info(f"Removed file {file_config.get('dest')}")
        elif file_config.get('state') == 'present':
            if 'src' in file_config:
                if not self._check_src_file_exists(file_config.get('src')):
                    raise InvalidTaskConfiguration(f"Source file {file_config.get('src')} not present.")
                self._copy_file(file_config.get('src'), file_config.get('dest'))

            if 'owner' in file_config:
                if not self._update_owner(file_config.get('dest'), file_config.get('owner')):
                    self.logger.error(f"Unable to update owner for {file_config.get('dest')}")
                else:
                    self.logger.info(f"Updated owner for {file_config.get('dest')} to {file_config.get('owner')}")

            if 'group' in file_config:
                if not self._update_group(file_config.get('dest'), file_config.get('group')):
                    self.logger.error(f"Unable to update group for {file_config.get('dest')}")
                else:
                    self.logger.info(f"Updated group for {file_config.get('dest')} to {file_config.get('group')}")

            if 'mode' in file_config:
                if not self._update_mode(file_config.get('dest'), file_config.get('mode')):
                    self.logger.error(f"Unable to update mode for {file_config.get('dest')}")
                else:
                    self.logger.info(f"Updated mode for {file_config.get('dest')} to {file_config.get('mode')}")
