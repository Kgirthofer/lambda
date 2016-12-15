from __future__ import print_function

import json
import urllib
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('Loading function')

ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')

import boto3
def lambda_handler(event,context):
    logger.info('got event{}'.format(event))
    instanceId = event['detail']['instance-id']
    instanceName = ec2.describe_instances(InstanceIds=[str(instanceId),])['Reservations'][0]['Instances'][0]['Tags'][0]
    print ("Instance Name: " + instanceName.get('Value'))
    print("Instance ID: " + instanceId)
    command = 'sh ##PUT_YOUR_COMMAND_HERE## ' + instanceName.get('Value')
    print("Command: " + command)
    ssmresponse = ssm.send_command(InstanceIds=['##instanceID_to_run_command_on##'], DocumentName='AWS-RunShellScript', Parameters= { 'commands': [command] } ) 
