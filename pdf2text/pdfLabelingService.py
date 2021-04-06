import uuid
import os
import shutil

from pdf2text.searchPdf import PdfDownloader
from pdf2text.pdf2xml import Pdf2xml
from pdf2text.xml2text import Xml2text


class PdfLabelingService:
    def __init__(self, downloader: PdfDownloader, pdf2xml: Pdf2xml, xml2text: Xml2text):
        self.downloader: PdfDownloader = downloader
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

        self.clear_cache_dir(uuid)

        return self.xml2text.articles
