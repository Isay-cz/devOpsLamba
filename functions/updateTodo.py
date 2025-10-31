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
        body = json.loads(event.get("body", "{}"))
        title = body.get("title")
        done = body.get("done")

        update_expr_parts = []
        expr_attr_values = {}

        if title is not None:
            update_expr_parts.append("title = :t")
            expr_attr_values[":t"] = title

        if done is not None:
            update_expr_parts.append("done = :d")
            expr_attr_values[":d"] = bool(done)

        if not update_expr_parts:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Nada que actualizar"})
            }

        update_expr = "SET " + ", ".join(update_expr_parts)

        resp = table.update_item(
            Key={"id": todo_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="ALL_NEW"
        )

        updated_item = resp.get("Attributes", {})

        return {
            "statusCode": 200,
            "body": json.dumps(updated_item)
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
