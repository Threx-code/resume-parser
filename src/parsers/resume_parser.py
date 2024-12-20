from typing import List, Dict, Any

from src.parsers.base.base_parser import BaseParser


class ResumeParser:

    def __init__(self, parser: BaseParser, criteria: Dict[str, str]):
        self.parser = parser
        self.criteria = criteria
        self.data = []

    def fetch_resume(self) -> List[Dict[str, Any]]:
        parser = self.parser
        parser.url(self.criteria)
        self.data.append(parser.parse_resume())
        return self.data
