
import sys

from util.s3_utils import display_buckets
from util.s3_utils import copy_file_to_s3
from util.config import config



util_ini = ''



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('usage: %s <file name > <config file>'%(sys.argv[0]))
        sys.exit()
    util_ini = sys.argv[2]

    # Read required information from Config file
    
    S3params = config(filename=util_ini, section='s3_config')
    csv_params = config(filename=util_ini, section='database_2_csv')

    # Require variables
    bucket = S3params['s3bucket']
    filepath = csv_params['path2csv']
    csv_file = sys.argv[1]  # this is going to be a command line arg.

    file_local_address = '{}/{}'.format(csv_params['path2csv'], csv_file)
    s3_dest = '{}/{}'.format(bucket, csv_file)
    copy_file_to_s3(file_local_address, bucket, s3_dest)