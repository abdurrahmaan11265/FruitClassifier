#!/bin/bash

# Exit early on errors
set -eu

# Ensure Python 3 is used
export PYTHONUNBUFFERED=true

# Install Python 3 virtual env
VIRTUALENV=.data/venv

if [ ! -d $VIRTUALENV ]; then
  python3 -m venv $VIRTUALENV
fi

if [ ! -f $VIRTUALENV/bin/pip ]; then
  curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | $VIRTUALENV/bin/python3
fi

# Install the requirements
$VIRTUALENV/bin/pip install -r requirements.txt

# Run the Python 3 server
$VIRTUALENV/bin/python3 app.py
