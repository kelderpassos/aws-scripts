import boto3
import logging


class SecretsManager():
    def __init__(self, credentials:dict[str, str]) -> None:
        session = boto3.Session(**credentials)
        self.client = session.client('secretsmanager')

    def list_secrets(self):
        try:
            response = self.client.list_secrets()
            return response['SecretList']
        except Exception as error:
            logging.error('Erro ao listar segredos: %s', error)
            raise error

    def check_existing_secret(self, name:str):
        secrets = self.list_secrets()

        for secret in secrets:
            if secret['Name'] == name:
                return True
        
        return False

    def get_secret_value(self, name: str, old_account_suffix: str, new_account_suffix: str):
        try:
            response = self.client.get_secret_value(SecretId=name)

            if response.get('Name').endswith(old_account_suffix):
                new_name = response.get('Name').replace(old_account_suffix, new_account_suffix)
                response['Name'] = new_name

            return response
        except Exception as error:
            logging.error('Erro ao recuperar valor dos segredos: %s', error)
            raise error
    
    def create_secret(self, value):
        new_secret = {
            'Name': value['Name'],
            'SecretString': value['SecretString'],
        }

        try:
            response = self.client.create_secret(**new_secret)
            return response
        except Exception as error:
            logging.error('Erro ao criar segredos: %s', error)
            raise error