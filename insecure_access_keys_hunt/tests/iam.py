from moto import mock_aws
import boto3
from src.iam.IamManager import IamManager

@mock_aws
def test_list_users():
    # Criar instância mockada do IAM
    iam = boto3.client("iam")
    iam.create_user(UserName="test-user")

    # Testar método list_users()
    iam_manager = IamManager()
    users = iam_manager.list_users()
    assert len(users) == 1
    assert users[0]["UserName"] == "test-user"

@mock_aws
def test_list_access_keys():
    # Criar instância mockada do IAM
    iam = boto3.client("iam")
    iam.create_user(UserName="test-user")
    access_key = iam.create_access_key(UserName="test-user")["AccessKey"]

    # Testar método list_access_keys()
    iam_manager = IamManager()
    users = iam_manager.list_users()
    access_keys = iam_manager.list_access_keys(users)

    assert len(access_keys) == 1
    assert access_keys[0][0]["AccessKeyId"] == access_key["AccessKeyId"]

if __name__ == "__main__":
    test_list_users()
    test_list_access_keys()
    print("Tests passed successfully.")
