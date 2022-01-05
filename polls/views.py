from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pdb

from datetime import datetime
import os
import socket
import requests
import json

import boto3
from boto3.dynamodb.conditions import Key


# authenticates DynamoDB session
session = boto3.Session(
    aws_access_key_id='FakeMyKeyId',
    aws_secret_access_key='FakeSecretAccessKey'
)

# connects to DynamoDB at port 8001
dynamodb = session.resource('dynamodb', endpoint_url='http://127.0.0.1:8001')

# create table if not existed
try:
    table = dynamodb.create_table(
        TableName='polls',
        KeySchema=[
            {
                'AttributeName': 'poll_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'creation_date',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'poll_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'creation_date',
                'AttributeType': 'N'
            },
            {
                "AttributeName": "show",
                "AttributeType": "N"
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        GlobalSecondaryIndexes=[
            {
                "IndexName": "show_index",
                "KeySchema": [
                    {"AttributeName": "show", "KeyType": "HASH"},
                    {"AttributeName": "creation_date", "KeyType": "RANGE"}
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": ["poll_id, username", "question", "responses", "counts"]
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            },
            # {
            #     "IndexName": "test_index",
            #     "KeySchema": [
            #         {"AttributeName":"poll_id","KeyType":"HASH"},
            #         {"AttributeName":"creation_date","KeyType":"RANGE"}
            #     ],
            #     "Projection": {
            #         "ProjectionType":"INCLUDE",
            #         "NonKeyAttributes": ["username", "question", "responses","counts"]
            #     },
            #     "ProvisionedThroughput": {
            #         "ReadCapacityUnits": 1,
            #         "WriteCapacityUnits": 1
            #     }
            # },
            {
                "IndexName": "poll_id_index",
                "KeySchema": [
                    {"AttributeName": "poll_id", "KeyType": "HASH"}
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": ["creation_date", "voters"]
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            }
        ]
    )
    print("Table created!")
except Exception:
    print("Table is already created. Moving on...")
    pass

now = datetime.now()
date_time = int(now.strftime("%Y%m%d%H%M%S"))

table = dynamodb.Table('polls')


# return all existing polls
def polls(request):

    # response = table.scan(
    #     IndexName="test_index"
    # )

    try:
        response = table.query(
            IndexName="show_index",
            Select="ALL_PROJECTED_ATTRIBUTES",
            KeyConditionExpression=Key('show').eq(1),
            ScanIndexForward=False
        )
    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 404
        return response
    return HttpResponse(json.dumps(response['Items']))


def get_poll(
        request,
        poll_id
):
    try:
        creation_date_query = table.query(
            IndexName="poll_id_index",
            # Select="ALL_PROJECTED_ATTRIBUTES",
            KeyConditionExpression=Key('poll_id').eq(poll_id),
            Limit=1
        )
        item = creation_date_query['Items']
        creation_date = item[0]['creation_date']

        item = table.get_item(
            Key={
                'poll_id': poll_id,
                'creation_date': creation_date
            },
        )
        print(item)

    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 404
        return response
    return HttpResponse(json.dumps(item['Item']))


# POST method for creating a poll given username, question, and list of responses
def create_poll(
        request
):
    body = json.loads(request.body)
    responses = body["responses"]
    question = body["question"]
    username = body["username"]
    try:
        poll_id_query = table.query(
            IndexName="show_index",
            Select="ALL_PROJECTED_ATTRIBUTES",
            KeyConditionExpression=Key('show').eq(1),
            ScanIndexForward=False,
            Limit=1
        )
        item = poll_id_query['Items']
        if len(item) != 0:
            poll_id = item[0]['poll_id']
            poll_id = poll_id + 1
        else:
            poll_id = 0

        poll_output = {
            "poll_id": poll_id,
            "username": username,
            "question": question,
            "responses": responses,
        }

        current = datetime.now()
        date_time_string = int(current.strftime("%Y%m%d%H%M%S"))

        counts_temp = [0] * len(responses)
        voters = []
        table.put_item(
            Item={
                'poll_id': poll_id,
                'creation_date': date_time_string,
                'username': username,
                'question': question,
                'responses': responses,
                'counts': counts_temp,
                'voters': voters,
                'show': 1
            },
        )
    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 409
        return response
    return HttpResponse(json.dumps(poll_output))


# POST method where user can vote on a response in a post given post_id, username, and vote (chosen response)
def post_vote(
        request,
        username,
        poll_id,
        choice
):
    try:
        creation_date_query = table.query(
            IndexName="poll_id_index",
            Select="ALL_PROJECTED_ATTRIBUTES",
            KeyConditionExpression=Key('poll_id').eq(poll_id),
            Limit=1
        )
        item = creation_date_query['Items']

        creation_date = item[0]['creation_date']

        vote_output = {
            "username": username,
            "vote": choice,
            "poll_id": poll_id
        }

        table.update_item(
            Key={
                "poll_id": poll_id,
                "creation_date": creation_date
            },
            UpdateExpression=f"ADD counts[{choice}] :v1 SET #V = list_append(#V,:v2)",
            ConditionExpression="not contains (#V, :v3)",
            ExpressionAttributeNames={
                "#V": 'voters'
            },
            ExpressionAttributeValues={
                ":v1": 1,
                ":v2": [username],
                ":v3": username
            },
            # ReturnValues="ALL_NEW"
        )
    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 409
        if e.__class__.__name__ == "ConditionalCheckFailedException":
            return {"error": "This user has already voted"}
        return response
    return HttpResponse(json.dumps(vote_output))


# checks health for polls
def check_health(request):
    try:
        response = table.query(
            IndexName="show_index",
            Select="ALL_PROJECTED_ATTRIBUTES",
            KeyConditionExpression=Key('show').eq(1),
            ScanIndexForward=False
        )
        items = response['Items']
        return HttpResponse(json.dumps(items))
    except Exception as e:
        response = HttpResponse(str(e))
        response.status_code = 404
        return response


# self register instance to registry
def self_register(api):
    registerurl = "http://localhost:8000/registry/polls"
    url = "http://" + socket.gethostbyname(socket.gethostname()) + ":" + os.environ["PORT"] + "/polls"
    r = requests.post(registerurl, data={"text": url})