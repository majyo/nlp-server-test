import sys
# print(sys.path)
# sys.path.append("/home/lihw/workspace/grobid-client/grobid_client_python")
import grobid_client as grobid


class Pdf2xml:
    def __init__(self, config_path):
        self.client = grobid.grobid_client(config_path=config_path)

    def process(self, workers):
        self.client.process("processFulltextDocument", input_path="../pdfcache", output="../xmlcache", n=workers)


if __name__ == "__main__":
    pdf2xml = Pdf2xml("/home/vsphere/Workspace/grobid_client/grobid_client_python/config.json")
    pdf2xml.process(workers=4)
