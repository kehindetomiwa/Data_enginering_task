import sys
import argparse
import csv
import os
import psycopg2
from util.config import config
import gzip
import zipfile
import subprocess



util_ini = ''


def move_data(table_a, filename):

    '''
    This function connects with postgresql,
    selects rows, dump data to cvs file and zip on the 
    fly
    '''
    params = config(filename=util_ini, section='postgresql')
    csv_params = config(filename=util_ini, section='database_2_csv')

    filepath = csv_params["path2csv"]
    print('file path is: ', filepath)

    if not os.path.exists(filepath):
        os.mkdir(filepath)

    if os.path.exists(filepath):

        # try connec to the database
        try:
            print(params)
            conn = psycopg2.connect(**params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            quit()

        cur = conn.cursor()
        #sql = "SELECT pk, id,title,decription,published_timestamp,last_update FROM {} LIMIT 5;".format(table_a)
        sql = "SELECT pk, id,title,decription,published_timestamp,last_update FROM {} ;".format(table_a)

        try:
            output_file = filepath + '/' + filename + '.csv'
            print('csv file: ', output_file)

            print('sql query: ', sql)
            cur.execute(sql)

            # with gzip.open(output_file,  'rb') as this_file:
            #     print(this_file)
            #    cur.copy_expert(copy_sql, this_file)
            #    cur.close()
            #    conn.commit()

            print('check 1')
            result = cur.fetchall()
            headers = [i[0] for i in cur.description]

            file_ = open(output_file, 'w', newline='', )
            print('check 2')
            csv_file = csv.writer(file_, delimiter=',',
                                  lineterminator='\r\n',
                                  quoting=csv.QUOTE_ALL,
                                  escapechar='\\')

            csv_file.writerow(headers)
            csv_file.writerow(result)

            cur.close()
            conn.commit()

            print("Zipping file")
            os.system('gzip ' + output_file)
            print("Data export successful.")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Data export error ...")
            quit()

        finally:

            conn.close()
    else:
        print('File path does not exist')


if __name__ == '__main__':
    '''
    This is for standalone test 
    '''

    parser = argparse.ArgumentParser(__file__, description="dump")
    parser.add_argument("--table", "-t", dest='table', help="table to copy", type=str, default="app")
    parser.add_argument("--csv_name", "-ncsv", dest='csv_file', help="output csv file", type=str, default="new")
    parser.add_argument("--config", "-cfg", dest='config', help="link to config file", type=str, default="util/config/database.ini")
    args = parser.parse_args()

    table = args.table    
    csv_file = args.csv_file
    util_ini = args.config


    move_data(table, csv_file)



