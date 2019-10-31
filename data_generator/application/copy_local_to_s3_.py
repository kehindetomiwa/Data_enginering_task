import os
import sys
from typing import Any, Union

from util.aws_utils import copy_file_to_s3

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

bucket: Union[str, Any] = os.getenv('s3Bucket')
file_path = os.getenv('csv_path')




if __name__ == "__main__":

    if len(sys.argv) < 1:
        print('usage: %s <file name > '%(sys.argv[0]))
        sys.exit()
    csv_file = sys.argv[1]  # this is going to be a command line arg.
    file_local_address = '{}/{}'.format(file_path, csv_file)
    s3_destination = '{}/{}'.format(bucket, csv_file)
    copy_file_to_s3(file_local_address, bucket, s3_destination)