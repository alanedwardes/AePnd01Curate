from parse import *
import subprocess
import boto3
import urllib

s3 = boto3.resource('s3')

IMAGEMAGICK = '/usr/bin/convert'
DOWNLOAD_PATH = '/tmp/image.jpg'

def handler(event, context):
  bucket_name = urllib.unquote(event['Records'][0]['s3']['bucket']['name'])
  key_name = urllib.unquote(event['Records'][0]['s3']['object']['key'])

  bucket = s3.Bucket(bucket_name)
  bucket.download_file(key_name, DOWNLOAD_PATH)

  params = [
    IMAGEMAGICK,
    DOWNLOAD_PATH,
    '-colorspace', 'gray',
    '-resize', '1x1',
    'txt:-'
  ]
  
  print('Invoking ' + ' '.join(params))
  process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  
  stdout = process.stdout.read()
  print('stdout: ' + stdout)
  
  stderr = process.stderr.read()
  print('stderr: ' + stderr)
  
  #0,0: (  0,  0,  0)  #000000  gray(0,0,0)
  result = stdout.splitlines()[1]
  print('result: ' + result)
  
  parsed = parse('0,0: ({:d},{:d},{:d})  #{hex:d}  gray({:d},{:d},{:d})', result)
  print(parsed)