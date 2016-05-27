import boto3

s3 = boto3.resource('s3')

def handler(event, context):
  bucket = event['Records'][0]['s3']['bucket']
  object = event['Records'][0]['s3']['object']

  return object['key']