## Python 3.8
## by alber.py

import sqlite3
from datetime import datetime


def create_table(cursor, table):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table} (
        id int primary key,
        location text,
        longitude text,
        latitude text,
        date timestamp
        )
        ''')


def delete_swipe(table, id):
    conn = sqlite3.connect('tinderLocationChanger.db')
    c = conn.cursor()
    c.execute(f'''
        DELETE FROM {table} 
        WHERE id='{id}';
    ''')
    conn.commit()
    conn.close()


def insert_into_table(table, dict_location):
    conn = sqlite3.connect('tinderLocationChanger.db')
    c = conn.cursor()
    create_table(cursor=c, table="locations")
    rows = int(count_table_rows(table="locations"))
    c.execute(f'INSERT INTO {table} VALUES (?, ?, ?, ?, ?)',
            (rows + 1, str(dict_location['location']), dict_location['longitude'], str(dict_location['latitude']), datetime.now()))
    conn.commit()
    conn.close()


def query_table_by_id(table, id):
    conn = sqlite3.connect('tinderLocationChanger.db')
    c = conn.cursor()
    c.execute(f'''
                SELECT * from {table} 
                WHERE id='{id}';''')
    result = c.fetchall()
    return result


def query_table(table="locations"):
    conn = sqlite3.connect('tinderLocationChanger.db')
    c = conn.cursor()
    c.execute(f'''SELECT * from {table}''')
    result = c.fetchall()
    return result


def count_table_rows(table="locations"):
    conn = sqlite3.connect('tinderLocationChanger.db')
    c = conn.cursor()
    c.execute(f'''SELECT count(*) from {table}''')
    rows = c.fetchall()[0][0]
    return rows


def get_location_data(location):
    conn = sqlite3.connect('tinderLocationChanger.db')
    c = conn.cursor()
    c.execute(f'''
    SELECT * from locations
    WHERE location='{location}';''')
    result = c.fetchall()
    lat = result[0][3]
    lon = result[0][2]
    return lat, lon


print(query_table(table="locations"))
#insert_into_table(table="locations", dict_location=loc)