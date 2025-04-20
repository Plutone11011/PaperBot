
from telegram.constants import ParseMode
import logging
import os


from datetime import datetime, timedelta


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


async def send_query_result(application, channel_id):
    pdfs = run_daily_arxiv_query()

    for pdf in pdfs:
        text = f"""<b>{pdf.title}</b>

<b>Authors</b>: {','.join(pdf.authors)}

{pdf.link}

{pdf.abstract}

{','.join(pdf.categories)}
Published: {pdf.published}"""

        await application.bot.send_message(chat_id=channel_id, text=text, parse_mode=ParseMode.HTML)