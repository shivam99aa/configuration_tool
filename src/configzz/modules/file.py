import logging
import sys
import os


class File:

    def __init__(self, ssh_client):
        self.logger = logging.getLogger(__name__)
        self.ssh_client = ssh_client

    def _check_dest_file_exists(self, file_path) -> bool:
        command = f'if [[ -f "{file_path}" ]]; then echo "file exists"; else echo "file missing"; fi'
        stdout, stderr = self.ssh_client.execute_command(command)

        if stdout[0].rstrip() == "file exists":
            return True
        elif stdout[0].rstrip() == "file missing":
            return False
        else:
            self.logger.error("Got unexpected output")
            return False

    def _check_src_file_exists(self, file_path) -> bool:
        if os.path.exists(file_path):
            return True
        else:
            return False

    def _update_owner(self, file_path, owner) -> bool:
        command = f'chown {owner}: {file_path}'
        stdout, stderr = self.ssh_client.execute_command(command)

    def _update_group(self, file_path, group):
        command = f'chgrp {group} {file_path}'
        stdout, stderr = self.ssh_client.execute_command(command)

    def _update_mode(self, file_path, mode):
        command = f'chmod {mode} {file_path}'
        stdout, stderr = self.ssh_client.execute_command(command)

    def _copy_file(self, src_file, dest_file):
        self.ssh_client.copy_file(src_file, dest_file)

    def _remove_file(self, file_path):
        command = f"rm {file_path}"
        stdout, stderr = self.ssh_client.execute_command(command)

    def handler(self, file_config: dict):
        self.logger.info("Installed package")
        self.logger.info(file_config)

        if 'dest' not in file_config:
            self.logger.error("Dest is required.")
            sys.exit(1)

        if file_config['state'] == 'absent':
            if not self._check_dest_file_exists(file_config['dest']):
                self.logger.info(f"{file_config['dest']} already absent")
            else:
                self._remove_file(file_config['dest'])
        elif file_config['state'] == 'present':
            if 'src' in file_config:
                if not self._check_src_file_exists(file_config['src']):
                    self.logger.error(f"{file_config['src']} is missing")
                    sys.exit(1)
                self._copy_file(file_config['src'], file_config['dest'])

            if 'owner' in file_config:
                self._update_owner(file_config['dest'], file_config['owner'])

            if 'group' in file_config:
                self._update_group(file_config['dest'], file_config['group'])

            if 'mode' in file_config:
                self._update_mode(file_config['dest'], file_config['mode'])