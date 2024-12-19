from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class ScrapperRequest:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': self.USER_AGENT}
        self.req = Request(self.url, headers=self.headers)
        self.page = urlopen(self.req)
        self.html_content = self.page.read().decode("utf-8")
        self.soup = BeautifulSoup(self.html_content, "html.parser")

    def get_soup(self):
        return self.soup

