import sys
import os
import re
import argparse
import mysql.connector
from mysql.connector import errorcode

def read_file(file: str):
  lines=''
  with open(file,'r') as f:
    text = f.read().rstrip()
    lines += text

  return lines

def get_select_titles(q: str):
  heads=[]
  try:
    sel = q[q.lower().index('select')+7:q.lower().index('from')-1]
    for ele in sel.split(','):
      if len(re.findall(' as ',ele,flags=re.I)) > 0:
        bits = re.split(' as ', ele, flags=re.I)
        string = bits[-1].strip("'")
        heads.append(f'"{string}"')
      else:
        bits = ele.strip().split(' ')
        heads.append(f'"{bits[-1]}"')
  finally:
    heads = []

  return heads

def main(argv=()):
  parser = argparse.ArgumentParser(description="Argument Parser for my sql query runner",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-u", "--user",     help="username",                   required=True)
  parser.add_argument("-p", "--password", help="password",                   required=True)
  parser.add_argument("-s", "--server",   help="SQL host server",            required=True)
  parser.add_argument("-P", "--port",     help="SQL host server port",       required=False, default=3306)
  parser.add_argument("-d", "--database", help="SQL database to connect to", required=True)
  parser.add_argument("query",            help="SQL query to run")
  parser.add_argument("results",          help="Where to store the results", default='results.csv')
  args = parser.parse_args()
  config = vars(args)
  
  runQuery(config)

def connect(config):
  try:
    cnx = mysql.connector.connect(
      host=config['server'],
      user=config['user'],
      database=config['database'],
      password=config['password'],
      port=config['port']
    )
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
    return None
  else:
    return cnx


def runQuery(config):

  query = read_file(config['query'])
  
  cnx = connect(config)

  if cnx is None:
    return
  
  else:
    mycursor = cnx.cursor()

    mycursor.execute(query)

    myresult = mycursor.fetchall()


    with open(config['results'], 'w') as f:
      f.write(','.join(get_select_titles(query)))
      f.write(os.linesep)
      for x in myresult:
        line=''
        for i in range(len(x)):
          line += f'"{x[i]}"'
          line += ','      
        f.write(f'{line[0:-1]}{os.linesep}')

if __name__ == "__main__":
  main(sys.argv)