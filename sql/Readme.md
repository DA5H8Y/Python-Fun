## SQL Queryer
Runs the SQL query provided as the on a SQL Database.

usage: sql_queryer.py [-h] -u USER -p PASSWORD -s SERVER [-P PORT] -d DATABASE query results

Argument Parser for my sql query runner

positional arguments:
  query                 SQL query to run
  results               Where to store the results

options:
  -h, --help            show this help message and exit
  -u USER, --user USER  username (default: None)
  -p PASSWORD, --password PASSWORD
                        password (default: None)
  -s SERVER, --server SERVER
                        SQL host server (default: None)
  -P PORT, --port PORT  SQL host server port (default: 3306)
  -d DATABASE, --database DATABASE
                        SQL database to connect to (default: None)

### Installation
```bash
python -m venv .env
source .env/bin/activate
python -m pip install -r requirements.txt
```

### Running
```bash
python -m venv .env
source .env/bin/activate

python ./sql_queryer.py -s 127.0.0.1 -u root -p password -d sandbox verification-method.sql VerifyMethod-results.csv
```
