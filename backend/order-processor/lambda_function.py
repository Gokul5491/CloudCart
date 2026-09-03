import json
import boto3

sns = boto3.client("sns", region_name="ap-south-1")

TOPIC_ARN = "arn:aws:sns:ap-south-1:611913894105:CloudCart-OrderNotifications"


def lambda_handler(event, context):

    for record in event["Records"]:

        raw_body = record["body"]

        print("RAW SQS MESSAGE:")
        print(repr(raw_body))

        try:
            message = json.loads(raw_body)

            order_id = message.get("orderId")
            customer = message.get("customer")
            total = message.get("total")

            print("ORDER RECEIVED")
            print("Order ID:", order_id)
            print("Customer:", customer)
            print("Total:", total)

            # Send notification through SNS
            sns.publish(
                TopicArn=TOPIC_ARN,
                Subject="CloudCart Order Confirmed",
                Message=(
                    f"Order ID: {order_id}\n"
                    f"Customer: {customer}\n"
                    f"Total: ₹{total}\n\n"
                    "Your CloudCart order has been received successfully."
                )
            )

            print("SNS NOTIFICATION SENT")

        except json.JSONDecodeError as e:
            print("JSON ERROR:", str(e))

    return {
        "statusCode": 200,
        "body": "Processed"
    }
