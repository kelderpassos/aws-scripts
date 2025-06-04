import os
from dotenv import load_dotenv

load_dotenv()

ORIGIN_CREDENTIALS: dict = {
    'aws_access_key_id': os.getenv('DEV_ACCESS_KEY'),
    'aws_secret_access_key': os.getenv('DEV_SECRET_KEY'),
    'region_name': os.getenv('REGION')
}


DESTINATION_CREDENTIALS: dict = {
    'aws_access_key_id': os.getenv('PRD_ACCESS_KEY'),
    'aws_secret_access_key': os.getenv('PRD_SECRET_KEY'),
    'region_name': os.getenv('REGION')
}
