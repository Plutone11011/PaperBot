
import logging
import asyncio
from telegram.ext import Application

from src.bot import send_query_result
from src.secret import get_secrets_telegram

logger = logging.getLogger()
logger.setLevel("INFO")



def lambda_handler(event, context):
    

    
    logger.info("Pulling secrets")
    secrets = get_secrets_telegram()

    logger.info("Setting up bot")
    application = Application.builder().token(secrets["BOT_TOKEN"]).build()

    try:
        asyncio.run(send_query_result(application, secrets["CHANNEL_ID"]))
    except Exception as e:
        # TODO differentiate errors
        logger.error(f"There was an error in sending content to channel {e}")

    return "OK"

    
    


