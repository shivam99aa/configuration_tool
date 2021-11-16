#!/bin/bash

# This installer script expect that you have python3 installed on your machine.

pip --version

if [ $? -eq 0 ]
then
  echo "pip already installed. Moving further..."
else
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python3 get-pip.py
fi

# Installing required package for configuration tool.
pip install -r requirements.txt

python3 setup.py install