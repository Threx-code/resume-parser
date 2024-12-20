from bs4 import BeautifulSoup

from src.parsers.sites.work_ua import WorkAuScrapper
from src.helpers.http_request import ScrapperRequest

if __name__ == "__main__":
    criteria = {
        "keywords": ["python", "developer"],
        "location": "kyiv",
        "experience": "2",
        "salary_from": "1000",
        "salary_to": "2000",
    }

    workAu = WorkAuScrapper()
    workAu.url(criteria)
    ee = workAu.parse_resume()



    print(ee)

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