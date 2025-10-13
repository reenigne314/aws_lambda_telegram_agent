from telegram_agent_aws.config import settings

def lambda_handler(event, context):
    print("**Event received**")
    print(event)
    print("**Context received**")
    print(context)
    return {
        "statusCode": 200,
        "body": "Lambda function executed successfully"
    }
    