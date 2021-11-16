# Configuration Tool

Basic configuration tool which can perform simple tasks on a debian based machine using SSH. This tool is inspired from Ansible.
This tool is tested on Ubuntu 18.04 machine yet. It might not work on other linux flavors.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)

## Installation
### Prerequisites:
- `python` 
- `pip`

To install pip:
```
sudo apt install python3-pip
pip3 install --upgrade pip
```
Make sure pip is upgraded to latest version.

### Installation Steps:
Make sure you have adequate permissions to run these commands. Use `sudo` if user privileges needs to be upgraded.
```
pip3 install -r requirements.txt
python3 setup.py install
```

## Usage:
The following command will run a tasks file ([php_setup/php_setup.yml](php_setup/php_setup.yml )) against a list of hosts ([php_setup/inventory.yml](php_setup/inventory.yml)) using the ([php_setup/config.yml](php_setup/config.yml)) configuration file.

Run the following command to configure servers:

`configzz -c php_setup/config.example.yml -i php_setup/inventory.yml php_setup/php_setup.yml`

For viewing help run:

`configzz -h`

## Architecture
In this tool modules are written for each tasks which need to be performed on remote servers. It then uses ssh protocol to configure remote servers.

### Modules
Modules are pluggable piece of code which can be integrated into the tool to add functionalities to perform various tasks. Currently only 3 modules are written which are present in the code. These modules are:- 

#### Package
Package module is used to install packages on remote machine. It currently supports following options:

`name`: It is a list which contains package names which need to be configured on remote machines.

`state`: It shows the state of packages on remote machines. Currently only two states are supported `present` and `absent`

#### File
File module is used to configure a file on remote machine. It currently supports following options:

`src`: Path of the source file on local machine.

`dest`: Path of destination file on remote machine.

`owner`: Name of owner of file on remote machine.

`group`: Name of group of file on remote machine.

`mode`: Mode of file on remote machine.

`state`: State of file on remote machine. Currently only two states are suported `present` and `absent`.

#### Service
Service module is used to configure a service on remote machine. It currenty supports following options:

`name`: Name of service on remote machine.

`state`: State of service on remote machine. Currently only three states are supported `stopped`, `running` and `restarted`.

### Utils
Apart from above modules there are various utils file which are also present in this tool. These utils file are used to perform various tasks. These are:

#### Config
This reads defaults configuration and if user provides a configuration file then default values are overwritten with user provided configuration. 
Currently following configuration values are supported:

- Log level for logging configuration
- Common SSH credentials i.e. `username`, `password` and `key`. These credentials will be overwritten by host specific creds.

#### Controller
This is used to read tasks file provided by user. Also this is responsible for generating a dictionary of module objects.

#### Defaults
This contains default values or configuration for the tool.

#### Exceptions
This contains custom exceptions for the tool.

#### Inventory
This reads inventory file provided by user. Currently following values are supported:

- name of the remote server.
- FQDN of the remote server on which SSH connection will be made.
- ssh credentials for remote server. It contains `username`, `password` and `key`. Either of password or key is expected. This overwrites common ssh credentials.

#### SSH
This is used to perform SSH operations on remote machine. At present it can perform three tasks:

- Create ssh connection to remote server.
- Execute a command on remote server.
- Copy a file from local machine to remote server.

