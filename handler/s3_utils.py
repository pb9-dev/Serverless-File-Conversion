import boto3
import os

# Initialize S3 client
s3_client = boto3.client('s3')

# Get bucket name from environment variables
BUCKET_NAME = os.getenv("BUCKET_NAME", "file-conversion-bucket-pipeline")

def fetch_file_from_s3(file_name):
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_name)
        return response['Body'].read(), None
    except Exception as e:
        return None, str(e)

def upload_to_s3(file_name, content, content_type):
    new_file_name = file_name.rsplit(".", 1)[0] + f".{content_type.split('/')[-1]}"
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=new_file_name,
            Body=content if isinstance(content, str) else content.getvalue(),
            ContentType=content_type
        )
        return new_file_name, None
    except Exception as e:
        return None, str(e)
