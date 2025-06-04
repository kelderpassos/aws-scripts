import logging

import boto3


class SecretsManager:
    """
    Utility class for managing AWS Secrets Manager secrets.
    Provides methods to list, check, retrieve, create, update, and delete secrets using boto3.
    """

    def __init__(self, credentials: dict[str, str]) -> None:
        """
        Initializes the SecretsManager with the provided AWS credentials.

        Args:
            credentials (dict[str, str]): Dictionary with AWS credentials
                (e.g., aws_access_key_id, aws_secret_access_key, region_name).
        """
        session = boto3.Session(**credentials)
        self.client = session.client("secretsmanager")

    def list_secrets(self):
        """
        Lists all secrets in AWS Secrets Manager, handling pagination.

        Returns:
            list: A list of dictionaries, each representing a secret.
        """
        secrets = []
        next_token = None

        try:
            while True:
                if next_token:
                    response = self.client.list_secrets(NextToken=next_token)
                else:
                    response = self.client.list_secrets()
                secrets.extend(response.get("SecretList", []))
                next_token = response.get("NextToken")
                if not next_token:
                    break
            return secrets
        except Exception as error:
            logging.error("Error listing secrets: %s", error)
            raise error

    def get_secret_value(self, name: str):
        """
        Retrieves the value of a secret by its name.

        Args:
            name (str): The name of the secret.

        Returns:
            dict: The secret value response from AWS.
        """
        try:
            response = self.client.get_secret_value(SecretId=name)
            return response
        except Exception as error:
            logging.error("Error retrieving secret value: %s", error)
            raise error

    def create_secret(self, value):
        """
        Creates a new secret.

        Args:
            value (dict): Dictionary containing at least the 'Name' key.

        Returns:
            dict: The AWS response for secret creation.
        """
        new_secret = {"Name": value["Name"]}

        try:
            response = self.client.create_secret(**new_secret)
            return response
        except Exception as error:
            logging.error("Error creating secret: %s", error)
            raise error

    def delete_secret(self, name: str):
        """
        Deletes a secret by its name, without recovery period.

        Args:
            name (str): The name of the secret.

        Returns:
            dict: The AWS response for secret deletion.
        """
        try:
            response = self.client.delete_secret(
                SecretId=name, ForceDeleteWithoutRecovery=True
            )
            return response
        except Exception as error:
            logging.error("Error deleting secret: %s", error)
            raise error

    def update_secret(self, value: dict):
        """
        Updates an existing secret.

        Args:
            value (dict): Dictionary with update data (e.g., SecretId, SecretString).

        Returns:
            dict: The AWS response for secret update.
        """
        try:
            response = self.client.update_secret(**value)
            return response
        except Exception as error:
            logging.error("Error updating secret: %s", error)
            raise error
