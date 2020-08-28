# SimpleSecretRotation

The python code is to rotate a simple secret(Username and password). The code is written in accordance with the rotation template provided by AWS[1].

PreRequisites:-

(1)Create the secret in AWS SecretsManager with the following key/value pair.

{ "username": "Test", "password": "Test" }

(2)Create a lambda function[2] and add the add the code.For simplicity, keep the lambda rotation function outside the VPC. To add secretsmanager permissions to invoke the lambda function, use the following command:-

 aws lambda add-permission --function-name <function-name> --action lambda:InvokeFunction --statement-id Secretsmanager --principal secretsmanager.amazonaws.com

(3) Add the following Enviornment Variables for the lambda function.

Key:- SECRETS_MANAGER_ENDPOINT                           
Value:- https://secretsmanager.us-east-1.amazonaws.com    

(4)Create a lambda function IAM role and attach the SecretsManagerReadWrite managed policy.

(5)Once done, click on edit rotation and select the lambda function we created in step(2) and hit save. The first rotation will be invoked after we hit the save button.

Referneces:-
[1]https://github.com/aws-samples/aws-secrets-manager-rotation-lambdas/blob/master/SecretsManagerRotationTemplate/lambda_function.py
[2]https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html
