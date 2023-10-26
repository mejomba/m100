import psycopg2
from configparser import ConfigParser


def config(filename=None, section=None):
    parser = ConfigParser()
    parser.read(filename)

    db_config = dict()
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f'section {section} not found')

    return db_config


def connect(conn, cur):
    if conn and cur:
        conn, cur, local_connection = conn, cur, False
    else:
        try:
            params = config('database.ini', 'xxxx')
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            local_connection = True
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            conn, cur, local_connection = None, None, None
    return conn, cur, local_connection


connect(None, None)

# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_table(auto_commit=None):
    conn, cur, local_connection = connect(None, None)
    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print(conn, cur, local_connection)
    query = """create table if not exists bank(bank_id serial primary key,
    balance integer, 
    user_id integer references travel_user (user_id))"""
    cur.execute(query)
    if auto_commit:
        conn.commit()
    # conn.commit()

# create_table(True)