from searchPdf import PdfSearcher
import json


class SearchPdfService:
    def __init__(self, pdf_searcher: PdfSearcher) -> None:
        self.searcher: PdfSearcher = pdf_searcher

    def search_pdfs(self, title: str, workers=4) -> str:
        self.searcher.fetch(title, workers)
        results = [{"id": i, "article": article.toDict()} for i, article in enumerate(self.searcher.articles)]
        return json.dumps(results)
