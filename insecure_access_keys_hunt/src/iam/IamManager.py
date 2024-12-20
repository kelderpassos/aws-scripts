import boto3


class IamManager:
    def __init__(self):
        self.client = boto3.client("iam")

    def list_users(self) -> list:
        return self.client.list_users()["Users"]

    def list_access_keys(self, users: list):
        all_access_key = []

        for user in users:
            access_key = self.client.list_access_keys(UserName=user["UserName"])
            all_access_key.append(access_key["AccessKeyMetadata"])

        return all_access_key
