import json

from typing import List
from typing import Dict


class Article:
    def __init__(self, json_obj=None):
        self.title: str = ""
        self.authors: List = []
        self.journal: str = ""
        self.year: str = ""
        self.smb: str = ""

        if json_obj:
            self.load(json_obj)

    def load(self, json_obj):
        def check_authors(authors):
            if not isinstance(authors, list):
                raise TypeError("Attribute \"authors\" must be a list.")
            for value in authors:
                if not isinstance(value, str):
                    raise TypeError("Value in \"authors\" must be a string.")

        try:
            if isinstance(json_obj, str):
                json_obj = json.loads(json_obj)
            self.title = json_obj["title"]
            self.authors = json_obj["authors"]
            self.journal = json_obj["journal"]
            self.year = json_obj["year"]
            self.smb = json_obj["smb"]
            check_authors(self.authors)
        except Exception:
            raise Exception("load article failed.")

    def dump(self):
        return json.dumps(self.__dict__)

    def toDict(self):
        return self.__dict__


if __name__ == "__main__":
    # a = Article()
    json_str = """
    {"title": "title1", "authors": ["author1", "author2"], "journal": "journal1", "year": "year1", "smb": "smb1"}
    """
    # a.load(json_str)
    # print(a.dump())
    b = Article(json_str)
    print(b.dump())
    print(b.toDict())




