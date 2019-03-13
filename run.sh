#!/bin/bash

python3 -m venv ./venv
source ./venv/bin/activate

pip install -r ./requirements.txt
pip install --upgrade pip

python ws-sniffer.py
