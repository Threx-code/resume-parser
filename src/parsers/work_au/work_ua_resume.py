from typing import Dict, List, Any
import re
from src.helpers.http_request import ScrapperRequest

class WorkAuResumeScrapper:

    sections = {
        "Profile": ["Profile", "Summary", "About Me"],
        "Skills": ["Skills", "Technologies"],
        "Education": ["Education", "Academic Background"],
        "Work Experience": ["Work Experience", "Employment"],
        "Languages": ["Languages", "Language Skills"],
        "Contacts": ["Contacts", "Contact Info"],
        "Certifications": ["Certification", "Certificates"]
    }

    def __init__(self, applicant_data : dict):
        self.applicant_data = applicant_data


    def get_resume(self) -> Dict[str, Any]:
        link = self.applicant_data.get('link', '')

        soup = ScrapperRequest(link).get_soup()
        applicants_dirty_data = soup.find_all("div", class_="mt-0")

        for data in applicants_dirty_data:
            summary_data = data.find("div", id="add_info").text if data.find("div", id="add_info") else None
            work_summary = {}
            if summary_data:
                work_summary =self._extract_sections(summary_data)


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


            user_data= {
                'employment': employment,
                'ready_to_work': ready_to_work,
                'city_of_residence': city_of_residence,
                'education_details': education_details,
                'work_summary': work_summary,
            }
            self.applicant_data['user_data'] = user_data

            return self.applicant_data

        return {}


    def _extract_sections(self, text_data):
        section_data = {}

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

