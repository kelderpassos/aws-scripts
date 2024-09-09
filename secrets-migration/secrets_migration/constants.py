import os
from dotenv import load_dotenv

load_dotenv()

ORIGIN_CREDENTIALS: dict = {
    'aws_access_key_id': os.getenv('ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('SECRET_ACCESS_KEY'),
    'aws_session_token': os.getenv('AWS_SESSION_TOKEN'),
    'region_name': os.getenv('REGION')
}


DESTINATION_CREDENTIALS: dict = {
    'aws_access_key_id': os.getenv('ACCESS_KEY_ID_2'),
    'aws_secret_access_key': os.getenv('SECRET_ACCESS_KEY_2'),
    'aws_session_token': os.getenv('AWS_SESSION_TOKEN_2'),
    'region_name': os.getenv('REGION')
}

OLD_ACCOUNT_PREFIX=os.getenv('OLD_ACCOUNT_SUFFIX')
NEW_ACCOUNT_PREFIX=os.getenv('NEW_ACCOUNT_SUFFIX')

