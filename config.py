import os

def _get_config_value(key, default):
    result = default
    if key in os.environ:
        result = os.environ.get(key)
    try:
        local_config = __import__('config_local')
        result = local_config.__dict__[key]
    except:
        pass
    return result

def config_value(key, default=None):
    value = _get_config_value(key, default)
    if value:
        globals()[key] = value

config_value('DB_CONNECTION', 
    "host='localhost' dbname='firehose' user='postgres' password='secret'")
config_value('SECRET_KEY')
