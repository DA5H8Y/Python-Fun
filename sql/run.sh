#! /usr/bin/bash

python -m venv .env
source .env/bin/activate

python ./sql_queryer.py -s 127.0.0.1 -u root -p password -d sandbox verification-method.sql VerifyMethod-results.csv
