import psycopg2
from os import sys, path
from glob import glob

def import_project_root():
    parentdir = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.insert(0,parentdir)

def create_database(connection):
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    sql_files = glob('scripts/*.sql')
    for sql_file in sorted(sql_files):
        print('running {}'.format(sql_file))
        with open(sql_file) as f:
            sql = f.read()
            cursor.execute(sql)
    conn.commit()
    return conn


