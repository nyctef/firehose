import os

DB_CONNECTION="host='localhost' dbname='firehose' user='postgres' password='secret'"

if 'DB_CONNECTION' in os.environ:
    DB_CONNECTION = os.environ.get('DB_CONNECTION')

try:
    local_config = __import__('config_local')
    DB_CONNECTION = local_config.DB_CONNECTION
except e:
    pass
