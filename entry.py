import boto3
import urllib

s3 = boto3.resource('s3')

def handler(event, context):
  bucket_name = urllib.unquote(event['Records'][0]['s3']['bucket']['name'])
  key_name = urllib.unquote(event['Records'][0]['s3']['object']['key'])

  bucket = s3.Bucket(bucket_name)
  object = bucket.Object(key_name).get()

  return object['Body']