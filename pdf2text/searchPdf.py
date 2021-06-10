from smb.SMBConnection import SMBConnection
import urllib.parse
import urllib.request
import re
import IPy
import json

import logging

from typing import Dict
from typing import Tuple

from pdf2text.article import Article

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
            self.articles = [(i, Article(article)) for i, article in enumerate(json_list)]

    def connect_to_smb(self, host, port=445, username="", password=""):
        self.connection = SMBConnection(username, password, "", "", use_ntlm_v2=True)
        result = self.connection.connect(host, port)
        logging.info(result)

    def get_pdfs(self):
        if not self.connection:
            self.connect_to_smb(self.DEFAULT_SMB)

        for i, article in self.articles:
            share_path = self._get_path(article.smb)
            print(share_path)
            localfile_path = "../pdfcache/%s.pdf" % i
            localfile = open(localfile_path, "wb")
            self.connection.retrieveFile(share_path[0], share_path[1], localfile)
            logging.info("download file succeed.")

    def _get_path(self, smb: str) -> Tuple[str, str]:
        smb_list: list = smb.split("/")
        share_dir: str = smb_list[3]
        share_file: str = smb_list[4]
        share_file = urllib.parse.unquote(share_file)
        return share_dir, share_file


class PdfDownloader:
    def __init__(self):
        self.connection = None
        self.DEFAULT_SMB = "192.168.40.10"

    def connect_to_smb(self, host, port=445, username="robin", password="smb@123"):
        self.connection = SMBConnection(username, password, "", "", use_ntlm_v2=True)
        result = self.connection.connect(host, port)
        logging.info(result)

    def get_pdf(self, smb: str, work_dir: str):
        if not self.connection:
            self.connect_to_smb(self.DEFAULT_SMB)

        share_path = self._get_path(smb)
        logging.debug(share_path)
        localfile_path = "cache/%s/pdfcache/0.pdf" % work_dir
        localfile = open(localfile_path, "wb")
        self.connection.retrieveFile(share_path[0], share_path[1], localfile)
        logging.info("download pdf file succeed.")

    def _get_path(self, smb: str) -> Tuple[str, str]:
        smb_list: list = smb.split("/")
        share_dir: str = smb_list[3]
        share_file: str = smb_list[4]
        share_file = urllib.parse.unquote(share_file)
        return share_dir, share_file


class UrlPdfDownloader:
    def get_pdf(self, url: str, work_dir: str):
        local_path = "cache/%s/pdfcache/0.pdf" % work_dir
        try:
            urllib.request.urlretrieve(url, local_path)
            logging.info("\033[1;47;40m[DOWNLOAD] download pdf %s file succeed.\033[0m" % work_dir)
        except Exception:
            logging.info("\033[1;33;40m[DOWNLOAD] download pdf %s file faild.\033[0m" % work_dir)
            logging.info("\033[1;33;40m[DOWNLOAD] [LOCATION] %s.\033[0m" % url)


if __name__ == "__main__":
    searcher = PdfSearcher("192.168.40.6", "8001", "searchpdf")
    searcher.fetch("The properties of graphene", 2)
    for i, article in searcher.articles:
        print(article.dump())
    # searcher.connect_to_smb(searcher.DEFAULT_SMB)
    # searcher.get_pdfs()
    # searcher._get_path(searcher.articles[0].smb)
