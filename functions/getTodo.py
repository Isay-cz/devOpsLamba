import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    # Si viene path /getTodo/{id}, intentamos leer un item
    path_params = event.get("pathParameters") or {}
    todo_id = path_params.get("id")

    try:
        if todo_id:
            # Obtener un solo item
            resp = table.get_item(Key={"id": todo_id})
            item = resp.get("Item")
            if not item:
                return {
                    "statusCode": 404,
                    "body": json.dumps({"error": "No existe el item"})
                }
            return {
                "statusCode": 200,
                "body": json.dumps(item)
            }
        else:
            # Scan completo (no es lo más eficiente en producción)
            resp = table.scan()
            items = resp.get("Items", [])
            return {
                "statusCode": 200,
                "body": json.dumps(items)
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
