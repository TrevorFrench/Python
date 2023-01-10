import boto3
import time
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='[ACCESS_KEY]',
                          aws_secret_access_key='[SECRET_ACCESS_KEY]',
                          aws_session_token='[SESSION_TOKEN]',
                          region_name='us-east-1')

# EXAMPLE OF HOW YOU WOULD FILTER THE RESULTS A TABLE SCAN RETURNS BY A COLUMN NAMED 'Year'
def scan_by_year(year):
    table = dynamodb.Table('[TABLE_NAME]')
    response = table.scan(
        FilterExpression=Key("Year").eq(year)
    )
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    with open('[OUTPUT_FILE.json]', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    f.close()
