import boto3
import os
import json
from boto3.dynamodb.conditions import Key

s3 = boto3.resource('s3',
                          aws_access_key_id='[ACCESS_KEY_ID]',
                          aws_secret_access_key='[SECRET_ACCESS_KEY]',
                          aws_session_token='[SESSION_TOKEN]',
                          region_name='us-east-1')

# Select Your S3 Bucket
your_bucket = s3.Bucket('[S3_BUCKET_NAME_NO_PREFIX')

output_file = r'[OUTPUT_FILE_PATH.json]'

output = []

# Iterate All Objects in Your S3 Bucket Over the for Loop
for s3_object in your_bucket.objects.all():

    #use below three line ONLY if you have sub directories available in S3 Bucket
    #Split the Object key and the file name.
    #parent directories will be stored in path and Filename will be stored in the filename
  
    #path, filename = os.path.split(s3_object.key)

    #Create sub directories if its not existing
    #os.makedirs(path)
    
    #Download the file in the sub directories or directory if its available. 
    #data = your_bucket.download_file(s3_object.key, path/filename)

    key = s3_object.key
    body = s3_object.get()['Body'].read()
    print(key)
    output.append(body)

with open(output_file, 'w', encoding='utf-8') as jsonf:
    for entry in output:
        entry = entry.decode('utf8').replace("'", '"')
        print(entry)
        json.dump(entry, jsonf)
        jsonf.write('\n')
