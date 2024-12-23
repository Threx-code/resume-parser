from src.helpers.scoring_system import ResumeSystem
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

    scoring_weights = {
        "skills": 0.4,
        "work_experience": 0.3,
        "education": 0.2,
        "certifications": 0.1,
    }

    desired_keywords = {
        "skills": ["python", "django", "flask", "sql", "html", "css", "javascript"],
        "work_experience": ["developer", "engineer", "software", "project"],
        "education": ["computer", "engineering", "technology", "science"],
        "certifications": ["certified", "certificate", "course"],
    }

    for resume in resume_list:
        user_data = WorkAuResumeScrapper({
            "title": resume.get('title', ''),
            "link": resume.get('link', ''),
            "applicant_name": resume.get('applicant_name', ''),
            "age": resume.get('age', ''),
            "city": resume.get('city', ''),
        }).get_resume()

        resumes.append(user_data)


    rs = ResumeSystem(scoring_weights, resumes, desired_keywords)
    st = rs.sort_resumes()

    for s in st:
        print(s)






