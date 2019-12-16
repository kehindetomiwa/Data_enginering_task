#!/usr/bin/env python
import os
import argparse
import time
import uuid
import numpy
import psycopg2
from faker import Faker
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

n_host = os.getenv('host')
db_port = os.getenv('db_port')
db_user = os.getenv('db_user')
db_name = os.getenv('db_name')
db_password = os.getenv('db_password')


#n_host = 'postgres'
#db_port = '5432'
#db_user = 'postgres'
#db_name = 'postgres'
#db_password = 'postgres'


def get_date_updated(date):
    """
    :param date:
    :return: updated date
    this method used timedelta to get a
    future time when application was modified
    """
    now = datetime.now()
    n_days_since_published = (now - date).days
    l_day = numpy.random.randint(n_days_since_published)
    l_weeks = numpy.random.randint(7)
    l_hours = numpy.random.randint(60)
    l_seconds = numpy.random.randint(60)
    l_minutes = numpy.random.randint(60)
    delta_time = timedelta(days=l_day,
                           seconds=l_seconds,
                           minutes=l_minutes,
                           hours=l_hours,
                           weeks=l_weeks
                           )
    return date + delta_time


def get_app_name_description():
    """
    This fucntion gets all the necessary components needed to
    generate the random sample. it is based on the faker
    library (see https://github.com/joke2k/faker)
    """
    name_dscp = []
    faker = Faker()

    # vocabulary used to generate random descriptions
    all_name_verb = ["motors", "gym", "shopping", "traffic", "posting"]
    all_name_type = ["mobile", "desktop", "web"]
    all_dscp_verb = ["Download", "Use"]

    # random selector
    app_verb = numpy.random.choice(all_name_verb, p=[0.3, 0.2, 0.1, 0.2, 0.2])
    app_type = numpy.random.choice(all_name_type, p=[0.4, 0.4, 0.2])
    dscp_verb = numpy.random.choice(all_dscp_verb, p=[0.4, 0.6])

    random_name = faker.name()
    name = random_name.replace(' ', '_')

    app_name = "{}_{}_{}_app".format(name, app_verb, app_type)
    app_dscp = "{} {} for quick access to reliable {} services....".format(dscp_verb, app_name, app_type)

    publish_ts = faker.date_time(tzinfo=None, end_datetime=None)

    # this ensures that the updated time is not before the the publish date
    update_ts = get_date_updated(publish_ts)

    name_dscp.append(app_name)
    name_dscp.append(app_dscp)
    name_dscp.append(str(publish_ts))
    name_dscp.append(str(update_ts))

    return name_dscp


def create_tables():
    """create table in the PostgreSQL database  """

    create_table = (
        '''
        CREATE TABLE IF NOT EXISTS app(
        pk BIGSERIAL NOT NULL PRIMARY KEY,
        id VARCHAR(256) UNIQUE,
        title VARCHAR(256),
        decription VARCHAR(2000),
        published_timestamp TIMESTAMP,
        last_update TIMESTAMP
    );''')

    conn = None
    try:

        print('Connecting to the PostgreSQL database ...')
        conn = psycopg2.connect(host=n_host,
                                database=db_name,
                                port=db_port,
                                user=db_user,
                                password=db_password)
        cur = conn.cursor()
        cur.execute(create_table)
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_app(n_row, table_a):
    '''
    insert rows after connecting to posstgresql
    '''
    conn = None
    try:

        print('Connecting to the PostgreSQL database ...')
        conn = psycopg2.connect(host=n_host,
                                database=db_name,
                                port=db_port,
                                user=db_user,
                                password=db_password)
        cur = conn.cursor()
        print('inserting into {} new rows to app table '.format(n_row))

        stop_flag = True
        t1 = time.time()

        while stop_flag:
            app_uuid = str(uuid.uuid4())
            app_name_dscp = get_app_name_description()

            sql = "INSERT INTO {} " \
                  "(id,title,decription,published_timestamp,last_update) " \
                  "VALUES(\'{}\',\'{}\',\'{}\'," \
                  "\'{}\',\'{}\')".format(table_a, app_uuid,
                                          app_name_dscp[0],
                                          app_name_dscp[1],
                                          app_name_dscp[2],
                                          app_name_dscp[3])
            cur.execute(sql)
            if n_row % 100 == 0:
                print('{} rows written'.format(n_row))
            n_row = n_row - 1
            stop_flag = False if n_row == 0 else True
        dt = time.time() - t1
        print('finished inserting into table in: {} seconds'.format(round(dt, 3)))

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    '''
    This is for standalone test 
    '''
    parser = argparse.ArgumentParser(__file__,
                                     description="data generator")
    parser.add_argument("--num", "-n",
                        dest='num_rows',
                        help="Number of rows to generate ",
                        type=int, default=10)

    args = parser.parse_args()
    table_rows = args.num_rows

    create_tables()
    insert_app(table_rows, 'app')
