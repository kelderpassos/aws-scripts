import boto3
from typing import List, Dict



class IamManager:
    def __init__(self) -> None:
        self.client = boto3.client("iam")

    def list_users(self) -> List[Dict[str, str]]:
        return self.client.list_users()["Users"]

    def list_access_keys(self, users: List[Dict[str, str]]) -> List[List[Dict[str, str]]]:
        all_access_key = []

        for user in users:
            access_key = self.client.list_access_keys(UserName=user["UserName"])
            all_access_key.append(access_key["AccessKeyMetadata"])
        return all_access_key
