import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    path_params = event.get("pathParameters") or {}
    todo_id = path_params.get("id")

    if not todo_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "id es requerido en la ruta"})
        }

    try:
        table.delete_item(Key={"id": todo_id})
        return {
            "statusCode": 204,
            "body": ""
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
