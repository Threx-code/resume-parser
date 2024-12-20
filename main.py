from src.parsers.work_au.work_ua_list import WorkAuListScrapper
from src.parsers.work_au.work_ua_resume import WorkAuResumeScrapper

if __name__ == "__main__":
    criteria = {
        "keywords": ["python", "developer"],
        "location": "kyiv",
        "experience": "2",
        "salary_from": "1000",
        "salary_to": "2000",
    }

    workAu = WorkAuListScrapper()
    workAu.url(criteria)
    resume_list = workAu.parse_resume()
    resumes = []

    for resume in resume_list:
        user_data = WorkAuResumeScrapper({
            "title": resume.get('title', ''),
            "link": resume.get('link', ''),
            "applicant_name": 'name',
            "age": resume.get('age', ''),
            "city": resume.get('city', ''),
        }).get_resume()

        print(user_data)

    # salary_from = criteria.get("salary_from", "")
    # salary_to = criteria.get("salary_to", "")
    #
    # query =  "-".join(criteria.get("keywords", []))
    # location = criteria.get("location", "")
    # experience = criteria.get("experience", "")
    # salary = criteria.get("salary", "")
    #
    # url = f"https://www.work.ua/en/resumes-{criteria.get('location', [])}-"
    #
    # urls = f"{url}{query}/?experience={experience}&salary={salary}"
    # print(urls)


    # sr = ScrapperRequest(urls)
    # soup = sr.get_soup()

    # drt = soup.find_all("div", class_="resume-link")
    # print(drt)
    # resumes = []
    # for resume in soup.select(".cv-item"):
    #     resumes.append({
    #         "name": resume.select_one(".cv-title").text.strip(),
    #         "link": resume.select_one("a")['href'],
    #         "details": resume.select_one(".cv-details").text.strip()
    #     })
    # print(resumes)










