import sys
import os
import argparse
from mysql import connector

def read_file(file: str):
  lines=''
  with open(file,'r') as f:
    text = f.read().rstrip()
    lines += text

  return lines

def get_select_titles(q: str):
  heads=[]
  sel = q.splitlines()[0]
  for ele in sel.split(','):
    if ' as ' in ele:
      bits = ele.split(' as ')
      string = bits[-1].strip("'")
      heads.append(f'"{string}"')
    else:
      bits = ele.strip().split(' ')
      heads.append(f'"{bits[-1]}"')
  
  return heads

def main(argv=()):
  parser = argparse.ArgumentParser(description="Argument Parser for my sql query runner",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-u", "--user",     help="username",                   required=False, default='')
  parser.add_argument("-p", "--password", help="password",                   required=False, default='')
  parser.add_argument("-s", "--server",   help="SQL host server",            required=True)
  parser.add_argument("-P", "--port",     help="SQL host server port",       required=False, default=3306)
  parser.add_argument("-d", "--database", help="SQL database to connect to", required=False, default='')
  parser.add_argument("query",            help="SQL query to run")
  parser.add_argument("results",          help="Where to store the results", default='results.csv')
  args = parser.parse_args()
  config = vars(args)
  
  run(config)
  

def run(config):

  query = read_file(config['query'])

  if query.startswith(('CONNECT','SHOW')):                 
    mydb = connector.connect(
      host=config['server'],
      user=config['user'],
      password=config['password'],
      port=config['port']
    )
  else:
    if config['database'] is '':
      raise RuntimeError('Database not provided.')
    else:
      mydb = connector.connect(
      host=config['server'],
      user=config['user'],
      password=config['password'],
      port=config['port']
    )
      
  mycursor = mydb.cursor()

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