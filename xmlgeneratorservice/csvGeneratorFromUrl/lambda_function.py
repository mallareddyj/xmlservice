import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    url = event["queryStringParameters"]["csvUrl"]
    # url = "https://docs.google.com/spreadsheets/d/1it2bRRPj4NgXVPTv2s_a9c1TOtkbC-4Ot0xsB0NKP74/edit?ts=6050bb98#gid=871212399"
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='csvtoxml')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('csvRequest')
    response = table.scan(FilterExpression=Attr('csvUrl').eq(url))
    items = response["Items"]
    
    for item in items:
        if item["completion"] == "finished":
            return{
                'statusCode': 200,
                'body': item["xmlUrl"]
            }
        elif item["completion"] == "pending":
            return{
                'statusCode': 201,
                'body': json.dumps(item["reqID"])
            }
        elif item["completion"] == "failed":
            return{
                'statusCode': 403,
                'body': json.dumps("unable to extract xml for the given csv")
            }
    
    id = str(uuid.uuid4().int)
    table.put_item(
        Item={
            'reqID': id,
            'csvUrl': url,
            'completion': 'pending',
            'xmlUrl': str("")
        }
        )
    queue.send_message(MessageBody='message', MessageAttributes={
        'id': {
            'StringValue': id,
            'DataType': 'String'
        },
        'csvUrl': {
            'StringValue': url,
            'DataType': 'String'
        }
    })
    return {
        'statusCode': 201,
        'body': json.dumps(id)
    }