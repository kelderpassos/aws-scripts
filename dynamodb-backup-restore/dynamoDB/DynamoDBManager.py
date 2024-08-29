import logging
from botocore.exceptions import ClientError
import boto3


class DynamoDBManager:
    def __init__(self, credentials: dict, region: str ) -> None:
        session = boto3.Session(
            aws_access_key_id = credentials['accessKeyId'],
            aws_secret_access_key = credentials['secretAccessKey'],
            aws_session_token = credentials['sessionToken'],
            region_name = region
        )

        self.client = session.client('dynamodb')
        self.region = region

    def _create_table(self, config):
        try:
            response = self.client.create_table(config)
            return response
        except Exception as error:
            logging.error('Erro ao criar tabelas: %s', error)
            raise error
        
    def list_tables(self):
        try:
            response = self.client.list_tables()
            main_tables = filter(lambda x: 'AmplifyDataStore' not in x, response['TableNames'])
            return list(main_tables)
        except Exception as error:
            logging.error('Erro ao listar tabelas: %s', error)
            raise error

    def scan_table(self, table: str, last_evaluated_key: dict = None):
        print('escaneando tabela ', table)
        print('----1----')

        params = {'TableName': table}

        if last_evaluated_key:
            params['ExclusiveStartKey'] = last_evaluated_key

        try:
            response = self.client.scan(**params)
            items = response['Items']
            if 'LastEvaluatedKey' in response:
                next_items = self.scan_table(table, response['LastEvaluatedKey'])
                items.extend(next_items)
                print('----2----')
            
            print('Itens exportados do DynamoDB')
            return items
        except Exception as error:
            logging.error('Erro ao escanear tabela: %s', error)
            raise error
        
    def write_items(self, table: str, items: list):
        print('escrevendo itens')

        try:
            for item in items:
                self.client.put_item(TableName = table, Item = item)
                print('-------')

            print('escrita finalizada')
        except ClientError as error:
            logging.error('Não foi possível escrever o item: %s', error)
