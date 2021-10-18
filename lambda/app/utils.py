"""
Utils
"""

import json
import boto3
from botocore.exceptions import ClientError
from app.exceptions import AwsSecretException


def get_secret(secret_name: str, secret_key: str = "token"):
    """
    Get secret value

    Parameters
    ----------
    secret_name : str
        Name of the secret, it could also be partial arn or arn
    secret_key : str
        Secret key

    Returns
    -------
    str
        Secret value
    """

    # Create a Secrets Manager client
    client = boto3.client(service_name="secretsmanager")

    try:
        secret_value = client.get_secret_value(SecretId=secret_name)
    except ClientError as exc:
        raise AwsSecretException() from exc

    return json.loads(secret_value["SecretString"])[secret_key]
