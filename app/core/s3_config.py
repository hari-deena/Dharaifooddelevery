import boto3
import os
from dotenv import load_dotenv

# Load environment variables
ENV_FILE = os.getenv('ENV_FILE', '.env')
load_dotenv(ENV_FILE)

# AWS Credentials

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ID')
AWS_REGION_NAME = os.getenv('AWS_REGION_ID')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_ID')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

bucket_name = AWS_BUCKET_NAME

