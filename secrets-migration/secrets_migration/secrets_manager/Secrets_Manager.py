import boto3
import logging


class SecretsManager():
    def __init__(self, credentials:dict[str, str], region: str) -> None:
        session = boto3.Session(
            aws_access_key_id = credentials['accessKeyId'],
            aws_secret_access_key = credentials['secretAccessKey'],
            aws_session_token = credentials['sessionToken'],
            region_name = region
        )

        self.client = session.client('secretsmanager')
        self.region = region

    def list_secrets(self):
        try:
            response = self.client.list_secrets()
            return response['SecretList']
        except Exception as error:
            logging.error('Erro ao listar segredos: %s', error)
            raise error
        
    def get_secret_value(self, name: str):
        try:
            response = self.client.get_secret_value(SecretId=name)
            print('SEGREDOS', response)

            return response
        except Exception as error:
            logging.error('Erro ao recuperar valor dos segredos: %s', error)
            raise error
        
        