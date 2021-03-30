from smb.SMBConnection import SMBConnection
import urllib.parse
import urllib.request
import re
import IPy
import json

import logging

from typing import Dict

from pdf2text.Article import Article

logging.basicConfig(level=logging.INFO)


class PdfSearcher:
    def __init__(self, host: str, port: str, path: str) -> None:
        def handle_errpr(host, port, path):
            port_pattern = r"(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$"
            try:
                IPy.IP(host)
            except ValueError:
                raise ValueError("Invalid host IP formation %s." % host)
            if not re.match(port_pattern, port):
                raise ValueError("Invalid port formation %s." % port)

        handle_errpr(host, port, path)
        self.url = "http://%s:%s/%s" % (host, port, path)
        self.articles = []
        self.connection = None
        self.DEFAULT_SMB = "192.168.40.10"

    def fetch(self, title: str, limit: int) -> None:
        query_path = urllib.parse.urlencode({"title": title, "limit": limit})
        query_url = "%s?%s" % (self.url, query_path)
        logging.info("open URL: %s" % query_url)
        with urllib.request.urlopen(query_url) as f:
            data = f.read().decode("utf-8")
            json_list: list = json.loads(data)["ArticleList"]
            self.articles = [Article(article) for article in json_list]

    def connect_to_smb(self, host, port=445, username="", password=""):
        self.connection = SMBConnection(username, password, "", "", use_ntlm_v2=True)
        result = self.connection.connect(host, port)
        logging.info(result)

    def get_pdf(self):
        pass


if __name__ == "__main__":
    searcher = PdfSearcher("192.168.40.10", "8001", "searchpdf")
    searcher.fetch("The properties of graphene", 2)
    for article in searcher.articles:
        print(article.dump())
    searcher.connect_to_smb(searcher.DEFAULT_SMB)
