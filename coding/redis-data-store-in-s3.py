import boto3
import redis
import csv
import json
from io import StringIO

AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
AWS_REGION = 'your_aws_region'

REDIS_HOST = 'your_redis_host'
REDIS_PORT = 6379
REDIS_PASSWORD = 'your_redis_password'

S3_BUCKET_NAME = 'your_s3_bucket_name'
S3_OBJECT_KEY = 'redis_data.csv'

def export_redis_data_to_s3():
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    
    redis_data = redis_client.hgetall('your_redis_key')
    
    csv_data = [['Key', 'Value']]
    for key, value in redis_data.items():
        csv_data.append([key, value])
    
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(csv_data)
    
    s3_client = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=S3_OBJECT_KEY, Body=csv_buffer.getvalue())

    print("Data exported to S3 successfully.")

if __name__ == "__main__":
    export_redis_data_to_s3()

