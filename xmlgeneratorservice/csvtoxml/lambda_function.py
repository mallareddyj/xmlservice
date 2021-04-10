import json
import boto3
import csv
import uuid
import os
from csvfromsheeturl import get_csv
from constants import TABLE_NAME, BUCKET_NAME, MAX_LIMIT
from xmlgenerator import XmlGenerator

def generate_xml(file_name):
    a = XmlGenerator()
    return a.generate_xml(file_name)

def lambda_handler(event, context):
    
    s3 = boto3.resource('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    s3 = boto3.resource('s3')
    # event = {"Records": [{"messageId": "530bf62c-46d3-46f9-ac15-bd07b3357cc8", "receiptHandle": "AQEBaM78nZFisKYljAAW5PbUjvATiNVFflpmbOv2KcEV7JzgNIvObW30+YcRvV7RlyLG9/TW73Mu/ZaNxlDRDbp5KfOLLQF5mCbuvONRfAnwEMCIaCvMCJf+wZq8GUCbWKbzTAfmzIQXnWetR5YODLYiPdjIZBxRzEGc/1IcGeG0ZTCAT0oxlE8GJTShvYWmFaZ5gbwBG1tClTOdp1RSYeh1Ljp4yvh/+swgFK7Q1rfOGK/U6oc8iw8rAwCZljxGSziOVkwHOcylFtjGOqQ6HD6sy9b5NDvLWQkhZVR0JrY+61PHKMiAd35fMpy85wfYzBKRueN20tC2uHcYL77qD9ucl+nb+Msl2Ryt8dUQa1FQPmq8QKUAQrjODdZl7N9cdnsm", "body": "message", "attributes": {"ApproximateReceiveCount": "1", "SentTimestamp": "1617905783763", "SenderId": "AROA6QKF7YMSKE2RPHGNK:csvGeneratorFromUrl", "ApproximateFirstReceiveTimestamp": "1617905783766"}, "messageAttributes": {"csvUrl": {"stringValue": "https://docs.google.com/spreadsheets/d/1twixOICCAo5eChSu5lCO5VT9Zrc2W4PPlva6axmhgyU/edit#gid=147909294", "stringListValues": [], "binaryListValues": [], "dataType": "String"}, "id": {"stringValue": "91353806392461813336424465734503933940", "stringListValues": [], "binaryListValues": [], "dataType": "String"}}, "md5OfMessageAttributes": "a18c654e27ad9a3a600b4cf42835cd1c", "md5OfBody": "78e731027d8fd50ed642340b7c9a63b3", "eventSource": "aws:sqs", "eventSourceARN": "arn:aws:sqs:us-east-2:997116068644:csvtoxml", "awsRegion": "us-east-2"}]} 
    # event = {"Records": [{"messageId": "530bf62c-46d3-46f9-ac15-bd07b3357cc8", "receiptHandle": "AQEBaM78nZFisKYljAAW5PbUjvATiNVFflpmbOv2KcEV7JzgNIvObW30+YcRvV7RlyLG9/TW73Mu/ZaNxlDRDbp5KfOLLQF5mCbuvONRfAnwEMCIaCvMCJf+wZq8GUCbWKbzTAfmzIQXnWetR5YODLYiPdjIZBxRzEGc/1IcGeG0ZTCAT0oxlE8GJTShvYWmFaZ5gbwBG1tClTOdp1RSYeh1Ljp4yvh/+swgFK7Q1rfOGK/U6oc8iw8rAwCZljxGSziOVkwHOcylFtjGOqQ6HD6sy9b5NDvLWQkhZVR0JrY+61PHKMiAd35fMpy85wfYzBKRueN20tC2uHcYL77qD9ucl+nb+Msl2Ryt8dUQa1FQPmq8QKUAQrjODdZl7N9cdnsm", "body": "message", "attributes": {"ApproximateReceiveCount": "1", "SentTimestamp": "1617905783763", "SenderId": "AROA6QKF7YMSKE2RPHGNK:csvGeneratorFromUrl", "ApproximateFirstReceiveTimestamp": "1617905783766"}, "messageAttributes": {"csvUrl": {"stringValue": "https://docs.google.com/spreadsheets/d/1it2bRRPj4NgXVPTv2s_a9c1TOtkbC-4Ot0xsB0NKP74/edit?ts=6050bb98#gid=871212399", "stringListValues": [], "binaryListValues": [], "dataType": "String"}, "id": {"stringValue": "4905020764764565905007089342660192496", "stringListValues": [], "binaryListValues": [], "dataType": "String"}}, "md5OfMessageAttributes": "a18c654e27ad9a3a600b4cf42835cd1c", "md5OfBody": "78e731027d8fd50ed642340b7c9a63b3", "eventSource": "aws:sqs", "eventSourceARN": "arn:aws:sqs:us-east-2:997116068644:csvtoxml", "awsRegion": "us-east-2"}]} 
    for message in event["Records"]:
        if "messageAttributes" in message:
            message_attributes = message["messageAttributes"]
            csvUrl = message_attributes["csvUrl"]["stringValue"]
            reqID = message_attributes["id"]["stringValue"]
            values_input = get_csv(csvUrl)
            response = table.get_item(Key={'reqID': reqID})
            item = response["Item"]
            if item["completion"] == "finished":
                return{
                    'statusCode':200,
                    'body': json.dumps("successful")
                }
            
            output = "/tmp/test"
            xml_files = []
            fileNo=1
            if len(values_input) != 0:
                for i in range(len(values_input[0])):
                    values_input[0][i] = values_input[0][i].replace(" ","")
                start = 1
                for i in range(MAX_LIMIT+1, len(values_input), MAX_LIMIT):
                    end = i
                    output_file = output + ".csv"
                    with open(output_file, 'w') as f:
                        write = csv.writer(f)
                        write.writerow(values_input[0])
                        write.writerows(values_input[start:end])
                    
                    xml_file = generate_xml(output_file)
                    new_xml_file = "/tmp/" + str(uuid.uuid4()) + ".xml"
                    os.rename(xml_file, new_xml_file)
                    xml_file = new_xml_file
                    s3_path = "xml/"+xml_file.split("/")[-1]
                    s3.meta.client.upload_file(xml_file, BUCKET_NAME, s3_path)
                    xml_file = "https://csvandxml.s3.us-east-2.amazonaws.com/" + s3_path
                    # xml_files[fileNo] = xml_file
                    xml_files.append(xml_file)
                    fileNo+=1
                    start = end
                
                output_file = output + ".csv"
                with open(output_file, 'w') as f:
                    write = csv.writer(f)
                    write.writerow(values_input[0])
                    write.writerows(values_input[start:])
                
                xml_file = generate_xml(output_file)
                new_xml_file = "/tmp/" + str(uuid.uuid4()) + ".xml"
                os.rename(xml_file, new_xml_file)
                xml_file = new_xml_file
                s3_path = "xml/"+xml_file.split("/")[-1]
                s3.meta.client.upload_file(xml_file, BUCKET_NAME, s3_path)
                xml_file = "https://csvandxml.s3.us-east-2.amazonaws.com/" + s3_path
                # xml_files[fileNo] = xml_file
                xml_files.append(xml_file)
                table.update_item(Key={'reqID': str(reqID)},
                UpdateExpression="set completion=:newDigest",
                ExpressionAttributeValues={":newDigest": "finished"},
                ReturnValues="UPDATED_NEW"
                )
                table.update_item(Key={'reqID': str(reqID)},
                UpdateExpression="set xmlUrl=:newDigest",
                ExpressionAttributeValues={":newDigest": json.dumps(xml_files)},
                ReturnValues="UPDATED_NEW"
                )
            else:
                table.update_item(Key={'reqID': str(reqID)},
                UpdateExpression="set completion=:newDigest",
                ExpressionAttributeValues={":newDigest": "failed"},
                ReturnValues="UPDATED_NEW"
                )
    
        return{
            'statusCode':200,
            'body': json.dumps("successful")
            }        

    return{
        'statusCode':200,
        'body': json.dumps("successful")
    }
