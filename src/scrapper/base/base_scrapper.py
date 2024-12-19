from abc import abstractmethod, ABC

class Scrapper(ABC):
    @abstractmethod
    def scrape(self):
        pass