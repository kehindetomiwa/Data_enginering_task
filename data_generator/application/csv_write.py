import argparse
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


n_host = os.getenv('host')
db_port = os.getenv('db_port')
db_user = os.getenv('db_user')
db_name = os.getenv('db_name')
db_password = os.getenv('db_password')

file_path = os.getenv('csv_path')


def move_data(table_a, file_name):
    """
    This function connects with postgresql,
    load data to pandas and zip data on the fly
    """

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    output_file = file_path + '/' + file_name + '.csv.gz'

    conn = psycopg2.connect(host=n_host,
                            database=db_name,
                            port=db_port,
                            user=db_user,
                            password=db_password)
    print("connected")

    sql_command = "SELECT pk, id,title,decription,\
                    published_timestamp,\
                    last_update FROM {} ;" \
                    .format(table_a)
    print(sql_command)

    data = pd.read_sql(sql_command, conn)
    data.to_csv(output_file, columns=['pk', 'id',
                                      'title', 'decription',
                                      'published_timestamp',
                                      'last_update'],
                compression='gzip')


if __name__ == '__main__':
    '''
    This is for standalone test 
    '''
    parser = argparse.ArgumentParser(__file__,
                                     description="dump")
    parser.add_argument("--table", "-t",
                        dest='table',
                        help="table to copy",
                        type=str,
                        default="app")
    parser.add_argument("--csv_name", "-ncsv",
                        dest='csv_file',
                        help="output csv file",
                        type=str,
                        default="new")

    args = parser.parse_args()
    table = args.table
    csv_file = args.csv_file

    move_data(table, csv_file)
