
from telegram.constants import ParseMode
import logging
from datetime import datetime, timedelta
import time

from src.arxiv.arxiv_connector import ArxivConnector




# Dummy query function you assume is already implemented
def run_daily_arxiv_query():
    arxiv = ArxivConnector()
    arxiv.set_query_by_dates(datetime.now() - timedelta(days=5), datetime.now())

    pdfs = arxiv.execute_paginated_query()
    
    logging.info(f"Retrieved {len(pdfs)} papers")
    return pdfs


async def send_query_result(application, channel_id):
    pdfs = run_daily_arxiv_query()

    for i, pdf in enumerate(pdfs):
        if i > 0 and i % 5 == 0:
            logging.info("Sleeping for 5 seconds...")
            time.sleep(10)
        text = f"""<b>{pdf.title}</b>

<b>Authors</b>: {','.join(pdf.authors)}

{pdf.link}

{pdf.abstract}

{','.join(pdf.categories)}
Published: {pdf.published}"""

        await application.bot.send_message(chat_id=channel_id, text=text, parse_mode=ParseMode.HTML)