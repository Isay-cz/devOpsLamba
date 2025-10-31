import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        title = body.get("title")
        if not title:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "title es requerido"})
            }

        item_id = str(uuid.uuid4())
        item = {
            "id": item_id,
            "title": title,
            "done": False
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps(item)
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "DynamoDB error", "detail": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Unhandled error", "detail": str(e)})
        }
