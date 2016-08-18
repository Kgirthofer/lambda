from __future__ import print_function

import json
import urllib
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).encode('utf8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("FILE NAME: " + key)
        print("CHECKING FOR UPCASE")
        if key.islower():
            print("ALREADY LOWERCASE - WE GOOD")
        else:
            print("HAS AT LEAST ONE UPPERCASE - LETS FIX THIS SHIT")
            lower = key.lower()
            print("ADJUSTING NAME TO THE FOLLOWING: " + lower)
            s3.copy_object(Bucket=bucket, CopySource=bucket+"/"+key, Key=lower)
            s3.delete_object(Bucket=bucket, Key=key)
        return lower
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
