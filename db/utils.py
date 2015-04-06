import config
import psycopg2

# force db output to be unicode for py2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

def get_connection():
    return psycopg2.connect(config.DB_CONNECTION)
