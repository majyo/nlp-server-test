from pdf2text.searchPdf import PdfSearcher
from pdf2text.searchPdf import PdfDownloader
from pdf2text.pdf2xml import Pdf2xml
from pdf2text.xml2text import Xml2text
from pdf2text.searchPdfService import SearchPdfService
from pdf2text.pdfLabelingService import PdfLabelingService


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
    lb = start_labeling_module()
    uuid = lb.create_cache_dir()
    lb.clear_cache_dir(uuid)
    print(uuid)
