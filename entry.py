import boto3

s3 = boto3.resource('s3')

def handler(event, context):
  bucket = s3.Bucket(event['Records'][0]['s3']['bucket']['name'])
  object = bucket.Object(event['Records'][0]['s3']['object']['key']).get()

  return object['Body']