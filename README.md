# SimpleSecretRotation

The python code is to rotate a simple secret(Username and password). The code is written in accordance with the rotation template provided by AWS[1].

PreRequisites:-

Create the secret in AWS SecretsManager with the following key/value pair.

{ "username": "", "password": "" }

Create a lambda function[2] and add the add the code.For simplicity, keep the lambda rotation function outside the VPC. To add secretsmanager permissions to invoke the lambda function, use the following command:-

Create a lambda function IAM role and attach the SecretsManagerReadWrite managed policy.

Once done, click on edit rotation and select the lambda function we created in step(2) and hit save. The first rotation will be invoked after we hit the save button.
