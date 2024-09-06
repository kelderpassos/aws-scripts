import os

from secrets_manager.Secrets_Manager import SecretsManager
from dotenv import load_dotenv

load_dotenv()

region = os.getenv('REGION')
env_variables: dict = {
    'accessKeyId': os.getenv('ACCESS_KEY_ID'),
    'secretAccessKey': os.getenv('SECRET_ACCESS_KEY'),
    'sessionToken': os.getenv('AWS_SESSION_TOKEN')
}

def execute():
    secrets_manager = SecretsManager(env_variables, region)
    secret_list = secrets_manager.list_secrets()
    
    for secret in secret_list:
        print('secret', secret)
        secrets_manager.get_secret_value(secret['Name'])

    

if __name__ == '__main__':
    execute()