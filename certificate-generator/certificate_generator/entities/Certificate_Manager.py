import boto3
import logging


class CertificateManager:
    def __init__(self, credentials: dict[str, str]):
        session = boto3.Session(**credentials)
        self.client = session.client('acm')

    def request_certificate(self):
        pass