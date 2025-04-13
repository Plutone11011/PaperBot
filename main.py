
from telegram.ext import Application
from telegram.constants import ParseMode
import logging
from zoneinfo import ZoneInfo
import os
from datetime import time

from datetime import datetime, timedelta
import dotenv


from src.arxiv.arxiv_connector import ArxivConnector


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Dummy query function you assume is already implemented
def run_daily_arxiv_query():
    arxiv = ArxivConnector()
    arxiv.set_query_by_dates(datetime.now() - timedelta(days=4), datetime.now())

    pdfs = arxiv.execute_query()
    
    logging.info(f"Retrieved {len(pdfs)} papers")
    return pdfs


async def send_query_result(application):
    pdfs = run_daily_arxiv_query()

    for pdf in pdfs:
        text = f"""<b>{pdf.title}</b>

<b>Authors</b>: {','.join(pdf.authors)}

{pdf.link}

{pdf.abstract}

{','.join(pdf.categories)}
Published: {pdf.published}"""

        await application.bot.send_message(chat_id=os.getenv("CHANNEL_ID"), text=text, parse_mode=ParseMode.HTML)


def main():
    logging.info("Setting up bot")
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Schedule the task daily at 12:00 (UTC+2)
    application.job_queue.run_daily(
        send_query_result,
        time=time(hour=15, minute=3, tzinfo=ZoneInfo("Europe/Berlin")),  # 12:00
        name="daily_query"
    )

    logging.info("Polling..")
    application.run_polling()

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
