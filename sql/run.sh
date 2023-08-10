#! /usr/bin/bash

python -m venv .env
source .env/bin/activate

python ./sql_queryer.py
