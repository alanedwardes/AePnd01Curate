from parse import *
import subprocess
import boto3
import urllib
import os

s3 = boto3.resource('s3')

IMAGEMAGICK = '/usr/bin/convert'
INPUT_PATH = '/tmp/input.jpg'
OUTPUT_PATH = '/tmp/output.jpg'
THRESHOLD = 5 # 0-255

def execute(params):
  print('Invoking ' + ' '.join(params))
  process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  
  stdout = process.stdout.read()
  print('stdout: ' + stdout)
  
  stderr = process.stderr.read()
  print('stderr: ' + stderr)
  
  return stdout

def handler(event, context):
  bucket_name = urllib.unquote(event['Records'][0]['s3']['bucket']['name'])
  key_name = urllib.unquote(event['Records'][0]['s3']['object']['key'])
  
  parts = key_name.split('/')
  root = parts[0]
  file = parts[-1]

  bucket = s3.Bucket(bucket_name)
  bucket.download_file(key_name, INPUT_PATH)

  analysis = execute([
    IMAGEMAGICK,
    INPUT_PATH,
    '-colorspace', 'gray',
    '-resize', '1x1',
    'txt:-'
  ])
  
  ## ImageMagick pixel enumeration: 1,1,255,srgb
  #0,0: (  0,  0,  0)  #000000  gray(0,0,0)
  parsed = parse('0,0: ({},{},{})  #{}  {type}({r:d},{g:d},{b:d})', analysis.splitlines()[1])
  print('Analysis type {0}. rgb: {1}, {2}, {3}'.format(parsed['type'], parsed['r'], parsed['g'], parsed['b']))
  
  if parsed['r'] < THRESHOLD and parsed['g'] < THRESHOLD and parsed['b'] < THRESHOLD:
    print('Image too dark, ignoring')
    return
  
  execute([
    IMAGEMAGICK,
    INPUT_PATH,
    '-resize', '1280x720',
    OUTPUT_PATH
  ])
  
  print(root)
  print(file)
  #bucket.upload_file(OUTPUT_PATH, os.path.join())
