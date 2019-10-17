#!/usr/bin/env python


import subprocess as sp
import shlex

'''
Generate data into postgresql DB

'''
#Todo:
    # Replace this script with Airflow dag 
    
proc = sp.Popen(shlex.split("./data_generator.py -n 50"), stderr=sp.PIPE, stdout=sp.PIPE)
stdout, stderr = proc.communicate()

print("stdout: %s" % stdout)
print("stderr: %s" % stderr)

'''
Dump DB data from postgres to CSV file
'''

'''
Move CSV file to S3 bucket
'''

'''
Move data from s3 to Redshift
'''
