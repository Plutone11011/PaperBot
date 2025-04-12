from datetime import datetime, timedelta
import feedparser
import requests


class ArxivConnector:

    def __init__(self):

        self.base_url = "http://export.arxiv.org/api/query?"
        self.submitted_date = None
        self.max_results = 10
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

    def execute_query(self):

        query = f"start={self.start}&max_results={self.max_results}" 
        if self.id_list is not None:
            query += f"&id_list={self.id_list}"

        search_query = None
        if self.submitted_date:
            search_query = f"search_query=submittedDate:{self.submitted_date}"

        url = f"{self.base_url}{query}" +  f"&{search_query}" if search_query is not None else ""
        
        arxiv_feed = requests.get(url).text
        arxiv_docs = feedparser.parse(arxiv_feed)

        for entry in arxiv_docs.entries:
            print(entry.id)
            print(entry.published)
            print(entry.title)
            print(entry.authors)
            for link in entry.links:
                if link.rel == 'alternate':
                    print(link.href)
                elif link.title == 'pdf':
                    print(link.href)
            all_categories = [t['term'] for t in entry.tags]
            print(all_categories)
            print(entry.summary)
            print("\n\n")


if __name__ == "__main__":

        arxiv = ArxivConnector()
        arxiv.set_query_by_dates(datetime.now() - timedelta(days=3), datetime.now())

        arxiv.execute_query()