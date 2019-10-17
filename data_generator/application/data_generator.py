#!/usr/bin/env python

import argparse
import time
# using UUID lib
# we can use UUID datatype in postgress
import uuid

import numpy
import psycopg2
from faker import Faker

from util.config import config


def get_app_name_description():
    '''
    This fucntion gets all the necessary components needed to 
    generate the random sample. it is based on the faker
    library (see https://github.com/joke2k/faker)
    '''
    name_dscp = []
    faker = Faker()


    # vocabulary used to generare random description
    all_name_verb = ["motors", "gym", "shopping", "traffic", "posting"]
    all_name_type = ["mobile", "desktop", "web"]
    all_dscp_verb = ["Download", "Use"]

    # random selector
    app_verb = numpy.random.choice(all_name_verb, p=[0.3, 0.2, 0.1, 0.2, 0.2])
    app_type = numpy.random.choice(all_name_type, p=[0.4, 0.4, 0.2])
    app_type = numpy.random.choice(all_name_type, p=[0.4, 0.4, 0.2])
    dscp_verb = numpy.random.choice(all_dscp_verb, p=[0.4, 0.6])


    randpm_name = faker.name()
    # list_random_name = randpm_name.split(' ')
    # name = numpy.random.choice(list_random_name,p=[0.4,0.6])
    name = randpm_name.replace(' ', '_')

    

    app_name = "{}_{}_{}_app".format(name, app_verb, app_type)
    app_dscp = "{} {} for quick access to reliable {} services....".format(dscp_verb, app_name, app_type)
    
    

    publush_ts = str(faker.date_time(tzinfo=None, end_datetime=None))
    update_ts = str(faker.date_time(tzinfo=None, end_datetime=None))
    # add_last_data = int()

    name_dscp.append(app_name)
    name_dscp.append(app_dscp)
    name_dscp.append(publush_ts)
    name_dscp.append(update_ts)

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
        params = config()

        print('Connecting to the PostgreSQL database ...')
        conn = psycopg2.connect(**params)
        # conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")

        cur = conn.cursor()

        # for command in create_tables:
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
        params = config()

        print('Connecting to the PostgreSQL database ...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        table_rows = n_row

        print('inserting into {} new rows to app table '.format(n_row))
        stop_flag = True
        t1 = time.time()
        while (stop_flag):
            # print('starting loop:{}'.format(n_row))
            app_uuid = str(uuid.uuid4())
            app_name_dscp = get_app_name_description()

            sql = "INSERT INTO {} (id,title,decription,published_timestamp,last_update) VALUES(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(
                table_a,
                app_uuid,
                app_name_dscp[0],
                app_name_dscp[1],
                app_name_dscp[2],
                app_name_dscp[3])
            # print('loop: {} ####{}'.format(n_row,sql))
            cur.execute(sql)
            if (n_row % 100 == 0):
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
    parser = argparse.ArgumentParser(__file__, description="data generator")
    parser.add_argument("--num", "-n", dest='num_rows', help="Number of rows to generate ", type=int, default=10)

    args = parser.parse_args()
    table_rows = args.num_rows

    create_tables()
    insert_app(table_rows, 'app')



