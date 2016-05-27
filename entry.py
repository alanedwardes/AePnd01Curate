import boto3

s3 = boto3.resource('s3')

def handler(event, context):
  return "hi"