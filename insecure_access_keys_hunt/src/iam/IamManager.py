import logging
from typing import Dict

from boto3.session import Session
from mypy.mypy_boto3_iam_package.mypy_boto3_iam import IAMClient
from mypy.mypy_boto3_iam_package.mypy_boto3_iam.type_defs import (
    AccessKeyMetadataTypeDef,
    UserTypeDef,
)


class IamManager:
    def __init__(self, profile: str | None = None) -> None:
        try:
            session: Session = Session(profile_name=profile)
            self.iam: IAMClient = session.client("iam")
        except Exception as err:
            logging.error(f"Erro ao se conectar ao cliente: {err}")
            exit(1)

    def list_users(self) -> list[UserTypeDef]:
        try:
            return self.iam.list_users()["Users"]
        except self.iam.exceptions.ClientError as err:
            logging.error(f"Erro ao buscar usuários: {err}")
            return []

    def list_access_keys(
        self, users: list[UserTypeDef]
    ) -> list[list[AccessKeyMetadataTypeDef]]:
        all_access_key = []

        try:
            for user in users:
                access_key = self.iam.list_access_keys(UserName=user["UserName"])
                all_access_key.append(access_key["AccessKeyMetadata"])
            return all_access_key
        except self.iam.exceptions.ClientError as err:
            logging.error(f"Erro ao listar chaves: {err}")
            return []

    def delete_access_keys(self, user: Dict[str, str]):
        print(user, 'USER')
        try:
            self.iam.delete_access_key(
                UserName=user["username"], AccessKeyId=user["key_id"]
            )
            print(f"Access Key {user['key_id']} deleted")
            return
        except self.iam.exceptions.ClientError as err:
            logging.error(f"Erro ao apagar chaves: {err}")
