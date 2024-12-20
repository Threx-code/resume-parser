from abc import ABC
from typing import Dict, List, Any
from bs4 import BeautifulSoup
import re
from src.helpers.http_request import ScrapperRequest
from src.parsers.base.base_parser import BaseParser


class WorkAuScrapper(BaseParser, ABC):
    URL = "https://www.work.ua/en/resumes-"
    BASE_URL = "https://www.work.ua"
    sections = {
        "Profile": ["Profile", "Summary", "About Me"],
        "Skills": ["Skills", "Technologies"],
        "Education": ["Education", "Academic Background"],
        "Work Experience": ["Work Experience", "Employment"],
        "Languages": ["Languages", "Language Skills"],
        "Contacts": ["Contacts", "Contact Info"],
        "Certifications": ["Certification", "Certificates"]
    }

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
            link = f"{self.BASE_URL}{resume.select_one('a')['href']}"
            title = resume.select_one("a").text.strip(),
            # resumes.append({
            #     "title": title,
            #     "link": link,
            #     "applicant_name": name,
            #     "age": age,
            #     "city": city,
            # })

            applicant = ScrapperRequest(link).get_soup()



            # find_all("div", class_="mt-lg")
            #  in the loop class="dl-horizontal
            applicants_dirty_data = applicant.find_all("div", class_="mt-0")

            # print(applicants_dirty_data)
            # applicants_dirty_data = applicant.find_all("div", class_="mt-lg")


            for data in applicants_dirty_data:
                summary_data = data.find("div", id="add_info").text if data.find("div", id="add_info") else None
                work_summary = {}
                if summary_data:
                    work_summary =self._extract_sections(summary_data)
                print(work_summary)

                employment = data.find("dt", text="Employment:").find_next_sibling("dd").text \
                    if data.find("dt", text="Employment:") else None
                ready_to_work = data.find("dt", text="Ready to work:").find_next_sibling("dd").text \
                    if data.find("dt", text="Ready to work:") else None

                city_of_residence = data.find("dt", text="City of residence:").find_next_sibling("dd").text \
                    if data.find("dt", text="City of residence:") else None

                education_data = data.find("h2", text="Education")
                education_details = []
                if education_data:
                    for education in education_data.find_next_siblings(["h2", "p"], class_="h4 strong-600 mt-lg sm:mt-xl"):
                        school_name = ''
                        description = ''
                        if education.name == "h2":
                            school_name = education.text.strip()
                        elif education.name == "p":
                            description = education.text.strip().replace("\n", " ")
                        education_details.append({
                            "school_name": school_name,
                            "description": description
                        })



                # print(summary)
            # print("\n\n\n\n\n\n")

        return resumes






    def _extract_sections(self, text_data):
        # Define sections and keywords

        """
        Splits text into sections based on predefined keywords.
        """
        section_data = {}
        # Create a regex pattern to identify section keywords
        pattern = "|".join([rf"({keyword})" for keywords in self.sections.values() for keyword in keywords])
        matches = list(re.finditer(pattern, text_data, re.IGNORECASE))

        for i, match in enumerate(matches):
            section_name = next((key for key, keywords in self.sections.items() if match.group(0).strip() in keywords),
                                None)
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text_data)
            content = text_data[start:end].strip()
            if section_name:
                section_data[section_name.lower()] = content.replace(" ", "\n").replace("\n", " ")

        return section_data












