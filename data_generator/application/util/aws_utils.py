import boto3


def display_buckets():
    s3 = boto3.resource('s3')
    for buckets in s3.buckets.all():
        print(buckets.name)


def copy_file_to_s3(file_path, bucket, s3_dest):
    s3_client = boto3.client('s3')
    print('[copy_file_to_s3] local file add: ', file_path)
    print('[copy_file_to_s3] s3 bucket: ', bucket)
    print('[copy_file_to_s3] s3 destination: ', s3_dest)
    s3_client.upload_file(file_path, bucket, s3_dest)
