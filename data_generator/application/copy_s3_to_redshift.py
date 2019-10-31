


import psycopg2
import time
import sys
from util.s3_utils import copy_file_to_s3







def main():
    util_ini = 'util/config/database.ini'
    rs_param = config(filename=util_ini, section='redshift') 
    
    hosturl = rs_param['host_url']
    database = rs_param['databas_name']
    rs_port = rs_param['port']
    user = rs_param['user']
    rs_password = rs_param['password']

    S3params = config(filename=util_ini, section='s3_config') 
    
    
    try: 

        con=psycopg2.connect(dbname= database, host=hosturl,
                        port= rs_port, user= user, 
                        password= rs_password)

        print("connected")
    except:
        ('Unable to connect')
                        
                        
    #Copy Command as Variable
    tablename = 'app'
    path_file = S3params['s3Bucket']
    IAM_role = rs_param['aws_iam_role']
    region =  rs_param['region']


    copy_command= '''
        copy {} from \
        's3://{}' 
        credentials` 'aws_iam_role={}' 
        delimiter '|' region {}; '''.format()

    try:

        #Opening a cursor and run copy query
        cur = con.cursor()
        cur.execute(copy_command)
        cur.close()
        print('copy succesuflly')
    except:
        print('failed to copy')

    con.commit()
    con.close()