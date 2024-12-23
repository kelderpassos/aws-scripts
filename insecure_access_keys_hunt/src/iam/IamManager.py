from boto3 import client, Session, session
import logging
from typing import List, Dict



class IamManager:
    def __init__(self, profile=None) -> None:
        try:
            aws_profile: Session = session.Session(profile_name=profile)
            self.iam = aws_profile.client("iam")
        except Exception as err:
            logging.error(f"Erro ao se conectar ao cliente: {err}")

    def list_users(self) -> List[Dict[str, str]]:
        try:
            return self.iam.list_users()["Users"]
        except self.iam.exceptions.ClientError as err:
            logging.error(f"Erro ao buscar usuários: {err}")
            return []

    def list_access_keys(
        self, users: List[Dict[str, str]]
    ) -> List[List[Dict[str, str]]]:
        all_access_key = []

        try:
            for user in users:
                access_key = self.iam.list_access_keys(UserName=user["UserName"])
                all_access_key.append(access_key["AccessKeyMetadata"])
            return all_access_key
        except self.iam.exceptions.ClientError as err:
            logging.error(f"Erro ao listar chaves: {err}")
            return []

