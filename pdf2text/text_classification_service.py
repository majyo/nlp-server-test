import uuid
import os
import shutil
import json
import requests

from nltk.tokenize import sent_tokenize

from pdf2text.searchPdf import UrlPdfDownloader
from pdf2text.pdf2xml import Pdf2xml
from pdf2text.xml2text import Xml2text
from nerModule import NER

from typing import Dict
from typing import List


class TextClassificationService:
    def __init__(self, downloader: UrlPdfDownloader, pdf2xml: Pdf2xml, xml2text: Xml2text):
        self.downloader: UrlPdfDownloader = downloader
        self.pdf2xml: Pdf2xml = pdf2xml
        self.xml2text: Xml2text = xml2text

    @classmethod
    def create_cache_dir(cls) -> str:
        dir_id: str = str(uuid.uuid4())
        os.makedirs("cache/%s/pdfcache/" % dir_id)
        os.makedirs("cache/%s/xmlcache" % dir_id)
        return dir_id

    @classmethod
    def clear_cache_dir(cls, uuid: str) -> None:
        shutil.rmtree("cache/%s" % uuid)

    def pdf_labeling(self, smb: str, p2x_workers: int = 4):
        uuid: str = self.create_cache_dir()

        self.downloader.get_pdf(smb, uuid)
        self.pdf2xml.process(uuid, p2x_workers)
        self.xml2text.parse_xml_dir("cache/%s/xmlcache" % uuid)
        self.sentence_label()
        result = json.dumps(self.xml2text.articles)

        self.xml2text.clear_articles()

        self.clear_cache_dir(uuid)

        return result

    def sentence_label(self) -> None:
        for article in self.xml2text.articles:
            # article["abstract"] = self.ner.predicte(article["abstract"])
            for paragraph in article["body"]:
                paragraph["texts"] = [self.process_sentence(sub_para) for sub_para in paragraph["texts"]]

    def process_sentence(self, text: str):
        sentences = sent_tokenize(text)
        results = []
        for sentence in sentences:
            data = json.dumps({"sentence": sentence})
            label = requests.post(url="http://127.0.0.1:8104/api/tcl", data=data)
            label = label.index(max(label))
            results.append({"sentence": sentence, "label": label})
        return results

