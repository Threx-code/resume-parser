from typing import List, Dict, Any


class ResumeSystem:

    def __init__(self, score_weights: Dict[str, Any], resumes: List[Dict[str, Any]], desired_keywords: Dict[str, Any]):
        self.resumes = resumes
        self.weight = score_weights
        self.desired_keywords = desired_keywords


    def score(self, resume: Dict[str, Any]) -> float:
        score = 0
        user_data = resume.get('user_data')
        for section, weight in self.weight.items():
            section_content = user_data.get("work_summary", {}).get(section, "").lower()

            if section_content:
                score += weight
                score += weight * 0.5 * sum(1 for keyword in self.desired_keywords[section] if keyword in section_content)
        return round(score, 2)


    def sort_resumes(self):
        for resume in self.resumes:
            resume["score"] = self.score(resume)

        return sorted(self.resumes, key=lambda x: x['score'], reverse=True)

