from datetime import datetime, timedelta
import feedparser
import requests
import logging
import time
from pydantic import BaseModel
from typing import Optional, List

class ArxivPDF(BaseModel):
    id: str
    title: str
    authors: List[str]
    link: str
    abstract: str
    categories: Optional[List[str]]
    published: Optional[datetime]

class ArxivConnector:

    def __init__(self):

        self.base_url = "http://export.arxiv.org/api/query?"
        self.submitted_date = None
        self.max_results = 5
        self.id_list = None
        self.start = 0

    

    def set_query_by_dates(self, start_date: datetime, end_date: datetime):
        start_date_formatted = start_date.strftime("%Y%m%d%H%M")
        end_date_formatted = end_date.strftime("%Y%m%d%H%M")
        self.submitted_date = f"[{start_date_formatted}+TO+{end_date_formatted}]"

        return self

    def set_max_results(self, max_results: int):
        self.max_results = max_results
        return self
    
    def set_id_list(self, id_list: str):
        self.id_list = id_list
        return self
    
    def set_start(self, start: int):
        self.start = start
        return self

    def execute_paginated_query(self):

        pdfs = self.execute_query()
        prev_pdfs = []
        while len(pdfs) - len(prev_pdfs) > 0:
            # time.sleep(10)
            self.start += self.max_results
            prev_pdfs.extend(pdfs)
            pdfs.extend(self.execute_query())
            logging.info(f"Length of PDFs retrieved {len(pdfs)}")

        
        return pdfs



    def execute_query(self) -> List[ArxivPDF]:

        query = f"start={self.start}&max_results={self.max_results}" 
        if self.id_list is not None:
            query += f"&id_list={self.id_list}"

        search_query = None
        if self.submitted_date:
            search_query = f"search_query=submittedDate:{self.submitted_date}"

        url = f"{self.base_url}{query}" +  f"&{search_query}" if search_query is not None else ""
        
        logging.info(f"Querying {url}")
        
        arxiv_feed = requests.get(url).text
        arxiv_docs = feedparser.parse(arxiv_feed)

        pdfs = []
        for entry in arxiv_docs.entries:
            
            pdf_link = ""
            for link in entry.links:
                try:
                    if link.title == 'pdf':
                        pdf_link = link.href
                except AttributeError:
                    pass

            pdfs.append(ArxivPDF(
                id=entry.id,
                title=entry.title.replace("\n", ""),
                authors=[author["name"] for author in entry.authors][:10],
                link=pdf_link,
                categories=[t['term'] for t in entry.tags][:10],
                abstract=entry.summary.replace("\n", ""),
                published=entry.published
            ))
            
        
        return pdfs

