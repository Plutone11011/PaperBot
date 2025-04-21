
import logging
import asyncio
from telegram.ext import Application

from src.bot import send_query_result
from src.secret import get_secrets_telegram


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    
    
    logging.info("Pulling secrets")
    secrets = get_secrets_telegram()

    logging.info("Setting up bot")
    application = Application.builder().token(secrets["BOT_TOKEN"]).build()

    try:
        asyncio.run(send_query_result(application, secrets["CHANNEL_ID"]))
    except Exception as e:
        # TODO differentiate errors
        logging.error(f"There was an error in sending content to channel {e}")

    return "OK"

if __name__ == "__main__":
    main()