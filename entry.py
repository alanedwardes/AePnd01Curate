import subprocess
import boto3
import urllib

s3 = boto3.resource('s3')

IMAGEMAGICK_IDENTIFY = '/usr/bin/identify'
DOWNLOAD_PATH = '/tmp/image.jpg'

def handler(event, context):
  bucket_name = urllib.unquote(event['Records'][0]['s3']['bucket']['name'])
  key_name = urllib.unquote(event['Records'][0]['s3']['object']['key'])

  bucket = s3.Bucket(bucket_name)
  bucket.download_file(key_name, DOWNLOAD_PATH)

  params = [
    IMAGEMAGICK_IDENTIFY,
    DOWNLOAD_PATH
  ]
  
  print('Invoking ' + ' '.join(params))
  process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  
  print('ffmpeg stdout: ' + process.stdout.read())
  print('ffmpeg stderr: ' + process.stderr.read())