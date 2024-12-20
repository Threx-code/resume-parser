from abc import ABC
from typing import Dict, List, Any
from src.helpers.http_request import ScrapperRequest
from src.parsers.base.base_parser import BaseParser


class WorkAuListScrapper(BaseParser, ABC):
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
        try:
            soup = ScrapperRequest(self.URL).get_soup()
            resumes = []
            dirty_resume_lists = soup.find_all("div", class_="resume-link")

            for resume in dirty_resume_lists:
                name_age_city = resume.find('p', class_="mt-xs mb-0").find_all("span")
                name = name_age_city[0].text
                age = name_age_city[1].text.replace("\xa0", " ") if len(name_age_city) > 1 else None
                city = name_age_city[2].text if len(name_age_city) > 2 else None
                link = f"{self.BASE_URL}{resume.select_one('a')['href']}"
                title = resume.select_one("a").text.strip()

                resumes.append({
                    "title": title,
                    "link": link,
                    "applicant_name": name,
                    "age": age,
                    "city": city,
                })

            return resumes
        except Exception as e:
            raise RuntimeError(f"An error occurred while parsing the resume: {e}") from e
