from typing import List, Dict, Any


class ResumeParser:

    def __init__(self, site: str, criteria: Dict[str, str]):
        self.site = site
        self.criteria = criteria
        self.data = []


    def fetch_resume(self) -> List[Dict[str, Any]]:
        if self.site == 'work_ua':
            from src.parsers.work_au import WorkAuScrapper
            scrapper = WorkAuScrapper()
            self.data = scrapper.scrape()
        return self.data
