import json
import requests
import asyncio
from telegram import Update, Bot
from telegram.ext import ContextTypes

from telegram_agent_aws.config import settings
from telegram_agent_aws.infrastructure.telegram.handlers import handle_text, handle_voice, handle_photo
from telegram_agent_aws.application.conversation_service.generate_response import get_agent_response



def check_and_set_webhook(bot_token: str, webhook_endpoint: str) -> dict:
    """
    Checks if a webhook exists for the Telegram bot.
    If the webhook doesn't exist or is different, sets it to the provided endpoint.
    
    Args:
        bot_token: The Telegram bot token
        webhook_endpoint: The webhook URL to set
        
    Returns:
        dict: Response from the API with status information
    """
    # Check current webhook info
    get_info_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    response = requests.get(get_info_url)
    webhook_info = response.json()
    
    if not webhook_info.get("ok"):
        return {"error": "Failed to get webhook info", "details": webhook_info}
    
    current_url = webhook_info.get("result", {}).get("url", "")
    
    # Check if webhook already exists and matches
    if current_url == webhook_endpoint:
        return {
            "status": "unchanged",
            "message": f"Webhook already set to {webhook_endpoint}",
            "webhook_info": webhook_info["result"]
        }
    
    # Set the webhook
    set_webhook_url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_endpoint}"
    response = requests.get(set_webhook_url)
    result = response.json()
    
    if result.get("ok"):
        return {
            "status": "updated",
            "message": f"Webhook set from '{current_url}' to '{webhook_endpoint}'",
            "result": result
        }
    else:
        return {
            "status": "error",
            "message": "Failed to set webhook",
            "result": result
        }


async def process_update(update_data: dict):

    _ = check_and_set_webhook(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_WEBHOOK_ENDPOINT)

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    
    update = Update.de_json(update_data, bot=bot)
    
    class WebhookContext:
        def __init__(self, bot):
            self.bot = bot
    
    context = WebhookContext(bot)
    
    try:
        if update.message:
            if update.message.text:
                await handle_text(update, context)
            elif update.message.voice:
                await handle_voice(update, context)
            elif update.message.photo:
                await handle_photo(update, context)
            else:
                await update.message.reply_text("Sorry, I don't support this message type yet.")
        else:
            print("Update doesn't contain a message")
    
    except Exception as e:
        print(f"Error processing update: {e}")
        if update.message:
            try:
                await update.message.reply_text("Sorry, something went wrong processing your message.")
            except Exception as reply_error:
                print(f"Failed to send error message: {reply_error}")
        raise
    finally:
        await bot.shutdown()


def lambda_handler(event, context):
    """
    AWS Lambda handler for Telegram webhook.
    
    The event contains the API Gateway payload with the Telegram update in the body.
    """
    print("**Event received**")
    print(json.dumps(event, indent=2))
    
    try:
        body = event.get("body", "{}")
        
        if isinstance(body, str):
            update_data = json.loads(body)
        else:
            update_data = body
        
        print("**Parsed update data**")
        print(json.dumps(update_data, indent=2))
    
        asyncio.run(process_update(update_data))
        
        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True})
        }
    
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "statusCode": 500,
            "body": json.dumps({"ok": False, "error": str(e)})
        }
