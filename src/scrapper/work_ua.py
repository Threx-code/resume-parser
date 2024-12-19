from abc import ABC
from .base.base_scrapper import Scrapper
from ..helpers.http_request import ScrapperRequest


class WorkAuScrapper(Scrapper, ABC):
    LINK = "https://www.work.ua/resumes-"

    def scrape(self):
        soup = ScrapperRequest(self.LINK).get_soup()
        links = soup.find_all("a", class_="pannel_module")
        formatted_data = self.format_data(links)



    def format_data(self, links):
        formatted_data = []
        for contents in links:
            link = contents.get("href")
            link_text = contents.text

            chunks = [chunk.strip() for chunk in link_text.strip().split("\n")]
            clean_chunks = [item for item in chunks if item]

            for i in range(0, len(clean_chunks), 2):
                title = clean_chunks[i]
                description = clean_chunks[i + 1]
                dt = {
                    'link': link,
                    'title': title,
                    'description': description
                }
                formatted_data.append(dt)

        return formatted_data




