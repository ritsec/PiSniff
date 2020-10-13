# !/usr/bin/python3
import psycopg2
import configparser
from time import sleep
from NetworkUser import NetworkUser
import database_queries


# Parse configuration file
config = configparser.ConfigParser()
config.read('config.ini')

db_info = config['database_info']

HOST = db_info['host']
DB_NAME = db_info['database_name']
TABLE_NAME = db_info['table_name']
USER = db_info['user']
PASSWORD = db_info['password']

LOCATION = config['location']['location']


def connect():
    """ Connect to the PostgreSQL database server using credentials and information from config.ini"""
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=HOST,
            database=DB_NAME,
            user=USER,
            password=PASSWORD
        )
        print('Connected to database:{} on host:{} as user:{}'.format(DB_NAME, HOST, USER))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return
    return conn


class Database:
    def __init__(self):
        """
        Attempt to establish connection to the database.

        Try connecting  5 times while waiting 5 seconds between each try.
        Raise error if connection fails.
        """
        for x in range(5):
            self.db = connect()
            if self.db is None:
                print('Connection failed, trying again {}/{} times.'.format(x+1, 5))
                sleep(5)
            else:
                break
        if self.db is None:
            raise psycopg2.DatabaseError('Failed to connect to database.')

    def send_data(self, network_user: NetworkUser):
        # Process network_user
        data = network_user.done()

        # Insert data into database
        cursor = self.db.cursor()
        cursor.execute(database_queries.INSERT_DATA_ENTRY.format(
            table_name=TABLE_NAME,
            timestamp=data[0],
            location_code=LOCATION,
            mac_address=data[1],
            start_time=data[2],
            end_time=data[3],
            avg_signal_strength=data[4],
            min_signal_strength=data[5],
            max_signal_strength=data[6]
        ))
        self.db.commit()
        cursor.close()

    def close(self):
        self.db.close()
