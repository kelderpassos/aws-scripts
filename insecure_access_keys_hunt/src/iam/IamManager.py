import boto3
from typing import List, Dict


class IamManager:
    def __init__(self, profile=None) -> None:
        profile = boto3.session.Session(profile_name=profile)
        self.iam = profile.client("iam")

    def list_users(self) -> List[Dict[str, str]]:
        return self.iam.list_users()["Users"]

    def list_access_keys(
        self, users: List[Dict[str, str]]
    ) -> List[List[Dict[str, str]]]:
        all_access_key = []

        for user in users:
            access_key = self.iam.list_access_keys(UserName=user["UserName"])
            all_access_key.append(access_key["AccessKeyMetadata"])
        return all_access_key
