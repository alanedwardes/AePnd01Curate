import boto3
import urllib

s3 = boto3.resource('s3')

def handler(event, context):
  key_name = urllib.unquote(event['Records'][0]['s3']['object']['key'])
  bucket_name = urllib.unquote(event['Records'][0]['s3']['bucket']['name'])

  bucket = s3.Bucket(bucket_name)
  object = bucket.Object(key_name).get()

  return object['Body']