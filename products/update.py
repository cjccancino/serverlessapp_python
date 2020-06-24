import json
import time
import logging
import os


import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the product.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # update the product in the database
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#product_name': 'name',
        },
        ExpressionAttributeValues={
          ':name': data['name'],
          ':description': data['description'],
          ':color': data['color'],
          ':price_cents': int,
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #product_name = :name, '
                         'description = :description, '
                         'color = :color, '
                         'price_cents = :price_cents, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'])
    }

    return response