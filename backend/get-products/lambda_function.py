import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("CloudCart-Products")


def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(item) for item in obj]

    if isinstance(obj, dict):
        return {key: convert_decimal(value) for key, value in obj.items()}

    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)

    return obj


def lambda_handler(event, context):

    response = table.scan()

    products = convert_decimal(response["Items"])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "products": products
        })
    }
