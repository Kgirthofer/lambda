from __future__ import print_function

import json
import urllib
import boto3
import botocore
import re

print('Loading function')

s3 = boto3.client('s3')
s3r = boto3.resource('s3')
regex = "\S*index.html$"

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    exists = False

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).encode('utf8')

    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        obj_hash = obj['ETag']
        print("FILE NAME: " + key)
        print("CHECKING BUCKET TYPE")
        if bucket == "bucket1":
            alt_bucket = "bucket2"
        else:
        print("Originating bucket is " + bucket)
        print("Alternating bucket is " + alt_bucket)
        exists = check_if_key_exists(alt_bucket, key)
        if exists:
            print("Object exists we need to check hash")
            alt_obj = s3.get_object(Bucket=alt_bucket, Key=key)
            alt_hash = alt_obj['ETag']
            print("Orig hash = " + obj_hash)
            print("Alt hash =  " + alt_hash)
            if alt_hash == obj_hash:
                print("Nothing to do - objects are the same")
            else:
                print("Objects are different - copying")
                s3.delete_object(Bucket=alt_bucket, Key=key)
        else:
            print("File does not exist in other bucket - copy")
            s3.copy_object(Bucket=alt_bucket, CopySource=bucket+"/"+key, Key=key)
        return alt_bucket
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
        
def check_if_key_exists(bucket, key):
    try:
        s3r.Object(bucket, key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False
        else:
            raise e
    else:
        exists = True
    return exists
    
