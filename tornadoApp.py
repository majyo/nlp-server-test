from nerModule import NER
from pdf2text.searchPdf import PdfSearcher
from pdf2text.searchPdf import PdfDownloader
from pdf2text.pdf2xml import Pdf2xml
from pdf2text.xml2text import Xml2text
from pdf2text.searchPdfService import SearchPdfService
from pdf2text.pdfLabelingService import PdfLabelingService

import tornado.web
import tornado.ioloop
import json


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
        # self.set_header('Access-Control-Max-Age', 1000)

    def prepare(self):
        if self.request.method == "GET":
            self.json_args = None
            return

        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = self.request.body
            return
        self.json_args = None

    def options(self):
        pass


class MainHandler(BaseHandler):
    def get(self):
        self.write("<p>This is a demonstration of the nlp platform.<p>")
        self.write("<p>To use this demo, please send JSON data to /api/allennlp/ner through POST request.<p>")


class NerHandler(BaseHandler):
    def initialize(self, ner):
        self.ner: NER = ner

    # def prepare(self):
    #     if self.request.method == "GET":
    #         self.json_args = None
    #         return
    #
    #     if self.request.headers.get("Content-Type", "").startswith("application/json"):
    #         self.json_args = self.request.body
    #         return
    #     self.json_args = None

    def get(self):
        self.write("<p>GET request is not supported so far. Please use POST request to access this handler.<p>")

    def post(self):
        if self.json_args:
            result = self.handle_ner()
            self.set_header("Content-Type", "text/plain")
            self.write(result)
            self.flush()
            self.finish()

    def handle_ner(self) -> str:
        args_dict: dict = json.loads(self.json_args)
        simple_mode: bool = False if args_dict["mode"] == "full" else True
        text = args_dict["text"]
        result = self.ner.predicte(text, simple_mode=simple_mode)
        return result


class PDFSearchHandler(BaseHandler):
    def initialize(self, search_pdf_service: SearchPdfService):
        self.search_pdf_service = search_pdf_service

    def get(self):
        pass

    def post(self):
        if self.json_args:
            title = json.loads(self.json_args)["title"]
            result = self.search_pdf_service.search_pdfs(title)

            self.set_header("Content-Type", "text/plain")
            self.write(result)
            self.flush()
            self.finish()


class PDFLabelingHandler(BaseHandler):
    def initialize(self, pdf_labeling_service: PdfLabelingService):
        self.pdf_labeling_service = pdf_labeling_service

    def get(self):
        pass

    def post(self):
        if self.json_args:
            smb = json.loads(self.json_args)["smb"]
            result = self.pdf_labeling_service.pdf_labeling(smb)

            self.set_header("Content-Type", "text/plain")
            self.write(result)
            self.flush()
            self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/allennlp/ner", NerHandler, dict(ner=start_ner_module())),
        (r"/api/pdfSearch", PDFSearchHandler, dict(search_pdf_service=start_search_module())),
        (r"/api/pdfLabeling", PDFLabelingHandler, dict(pdf_labeling_service=start_labeling_module()))
    ])


def start_ner_module():
    ner_instance = NER()
    ner_instance.load_model()
    return ner_instance


def start_search_module():
    searcher = PdfSearcher("192.168.40.10", "8001", "searchpdf")
    search_service = SearchPdfService(searcher)
    return search_service


def start_labeling_module():
    pdf_downloader = PdfDownloader()
    pdf2xml = Pdf2xml("/home/vsphere/Workspace/grobid_client/grobid_client_python/config.json")
    xml2text = Xml2text()
    labeling_service = PdfLabelingService(pdf_downloader, pdf2xml, xml2text)
    return labeling_service


if __name__ == "__main__":
    app = make_app()
    app.listen(8009)
    print("Starting App...")
    tornado.ioloop.IOLoop.current().start()
