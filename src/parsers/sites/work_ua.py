from abc import ABC
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from src.helpers.http_request import ScrapperRequest
from src.parsers.base.base_parser import BaseParser


class WorkAuScrapper(BaseParser, ABC):
    URL = "https://www.work.ua/en/resumes-"
    BASE_URL = "https://www.work.ua"

    def url(self, criteria: Dict[str, str]):
        query = "-".join(criteria.get("keywords", []))
        location = criteria.get("location", "")
        experience = criteria.get("experience", "")
        salary_from = criteria.get("salary_from", "")
        salary_to = criteria.get("salary_to", "")
        employment = criteria.get("employment", "")

        salary = f"salaryto={salary_to}" if salary_to is not None else f"salaryfrom={salary_from}"

        self.URL = f"{self.URL}{location}-{query}/?experience={experience}&{salary}&employment={employment}"



    def parse_resume(self) -> List[Dict[str, Any]]:
        soup = ScrapperRequest(self.URL).get_soup()
        resumes = []
        dirty_resume_lists = soup.find_all("div", class_="resume-link")


        for resume in dirty_resume_lists:
            name_age_city = resume.find('p', class_="mt-xs mb-0").find_all("span")
            name = name_age_city[0].text
            age = name_age_city[1].text.replace("\xa0", " ") if len(name_age_city) > 1 else None
            city = name_age_city[2].text if len(name_age_city) > 2 else None
            resumes.append({
                "job_title": resume.select_one("a").text.strip(),
                "link": f"{self.BASE_URL}{resume.select_one('a')['href']}",
                "applicant_name": name,
                "age": age,
                "city": city,
            })

        return resumes








