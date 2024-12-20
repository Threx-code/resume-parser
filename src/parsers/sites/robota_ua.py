from abc import ABC
from typing import Dict, List, Any

from src.helpers.http_request import ScrapperRequest
from src.parsers.base.base_parser import BaseParser

class RobotaScrapper(BaseParser, ABC):
    URL = "https://www.robota.ua/cv-"

    def url(self, criteria: Dict[str, str]):
        query = "-".join(criteria.get("keywords", []))
        location = criteria.get("location", "")
        experience = criteria.get("experience", "")
        salary = criteria.get("salary", "")

        self.URL = f"{self.URL}{query}/?region={location}&experience={experience}&salary={salary}"

    def parse_resume(self) -> List[Dict[str, Any]]:
        soup = ScrapperRequest(self.url).get_soup()
        resumes = []

        for resume in soup.select(".resume-card"):
            resumes.append({
                "name": resume.select_one(".resume-title").text.strip(),
                "link": resume.select_one("a")["href"],
                "details": resume.select_one(".resume-details").text.strip()
            })

        return resumes



