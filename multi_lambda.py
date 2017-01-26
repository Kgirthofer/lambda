from __future__ import print_function

import json
import boto3 

lambda = boto3.client('lambda')
functions = ['function1', 'funtion2']

def lambda_handler(event, context):
    print("Loading Function...")
    try:
        for function in functions:
            lambda.invoke(FunctionName=function, Payload=dumps(event))
    except Exception as e:
        print(e)
        print('Error getting running lambda')
        raise e
