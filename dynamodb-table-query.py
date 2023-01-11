import boto3
import time
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='[ACCESS_KEY]',
                          aws_secret_access_key='[SECRET_ACCESS_KEY]',
                          aws_session_token='[SESSION_TOKEN]',
                          region_name='us-east-1')

table = dynamodb.Table('[TABLE_NAME]')
    response = table.query(
        KeyConditionExpression=Key('[KEY_NAME]').eq(year) & Key('[KEY_NAME]').eq('')
    )
    return response['Items']
