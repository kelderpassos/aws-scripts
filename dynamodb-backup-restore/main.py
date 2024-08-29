from dynamoDB.DynamoDBManager import DynamoDBManager
import os

from dotenv import load_dotenv

load_dotenv()
region = os.getenv('REGION')
env_variables: dict = {
    'accessKeyId': os.getenv('ACCESS_KEY_ID'),
    'secretAccessKey': os.getenv('SECRET_ACCESS_KEY'),
    'sessionToken': os.getenv('AWS_SESSION_TOKEN')
}
temp_tables = ['temp-car_cpfcnpj']
definitive_tables = ['agrodesk-saas-persistent-infra-stg-car-cpfcnpj-table']

def execute():
    dynamodb = DynamoDBManager(env_variables, region)

    for table in temp_tables:
        table_items = dynamodb.scan_table(table)

    for table in definitive_tables:
        dynamodb.write_items(table, table_items)

if __name__ == '__main__':
    execute()
