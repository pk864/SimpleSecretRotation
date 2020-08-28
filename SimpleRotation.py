import boto3
import logging
import os
import time
import unicodedata
import base64
import json
from botocore.vendored import requests
from botocore.exceptions import ClientError
#from json import JSONEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    print('---- Inside the lambda_handler ----')
    print('Secret arn:')
    
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    # Setup the client
    service_client = boto3.client('secretsmanager', endpoint_url=os.environ['SECRETS_MANAGER_ENDPOINT'])

    if step == "createSecret":
        create_secret(service_client, arn, token)

    elif step == "setSecret":
        set_secret(service_client, arn, token)

    elif step == "testSecret":
        test_secret(service_client, arn, token)

    elif step == "finishSecret":
        finish_secret(service_client, arn, token)

    else:
        raise ValueError("Invalid step parameter")

#grabbing current password from secretsmanager
	

def create_secret(service_client, arn, token):

    mysecretresponse = service_client.describe_secret(SecretId=arn)
    print('mysecretresponse')

    try:

        # Generate a random password
        print('Generating new password')
        
        current_dict = get_secret_dict(service_client, arn, "AWSCURRENT")
        passwd = service_client.get_random_password(ExcludeCharacters='/@"\'\\', PasswordLength=30)
        current_dict['password'] = passwd['RandomPassword']
        

        # Put the secret
        service_client.put_secret_value(SecretId=arn, ClientRequestToken=token, SecretString=json.dumps(current_dict), VersionStages=['AWSCURRENT'])
        logger.info("createSecret: Successfully put secret for ARN %s and version %s." % (arn, token))

        
        

    except Exception as e:
        print("Error")
        print(e)
        return False


def set_secret(service_client, arn, token):
    print('------ Inside set_secret ------')
    print('nothing to be done here left because secret manager needs to call this')
    return True


def test_secret(service_client, arn, token):
    print('------ Inside test_secret ------')
    print('nothing to be done here left because secret manager needs to call this')
    return True

def finish_secret(service_client, arn, token):
    print('------ Inside finish_secret ------')
    print('nothing to be done here left because secret manager needs to call this')
    return True
    
def get_secret_dict(service_client, arn, stage, token=None):
    """Gets the secret dictionary corresponding for the secret arn, stage, and token
    This helper function gets credentials for the arn and stage passed in and returns the dictionary by parsing the JSON string
    Args:
        service_client (client): The secrets manager service client
        arn (string): The secret ARN or other identifier
        token (string): The ClientRequestToken associated with the secret version, or None if no validation is desired
        stage (string): The stage identifying the secret version
    Returns:
        SecretDictionary: Secret dictionary
    Raises:
        ResourceNotFoundException: If the secret with the specified arn and stage does not exist
        ValueError: If the secret is not valid JSON
    """
    required_fields = ['host', 'username', 'password']

    # Only do VersionId validation against the stage if a token is passed in
    if token:
        secret = service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage=stage)
    else:
        secret = service_client.get_secret_value(SecretId=arn, VersionStage=stage)
    plaintext = secret['SecretString']
    secret_dict = json.loads(plaintext)

    # Run validations against the secret

    # Parse and return the secret JSON string
    return secret_dict
