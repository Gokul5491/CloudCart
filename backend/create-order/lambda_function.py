import json
import boto3
import uuid
sqs = boto3.client("sqs", region_name="ap-south-1")
QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/611913894105/CloudCart-Orders"
def lambda_handler(event, context):
    body = json.loads(event["body"]) if isinstance(event.get("body"), str) else event
    order = {
        "orderId": "ORD-" + str(uuid.uuid4())[:8],
        "customer": body.get("customer"),
        "total": body.get("total")
    }
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(order)
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Order submitted successfully",
            "order": order
        })
    }
