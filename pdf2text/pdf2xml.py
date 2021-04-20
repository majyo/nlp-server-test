import sys
# print(sys.path)
# sys.path.append("/home/lihw/workspace/grobid-client/grobid_client_python")
import grobid_client as grobid


class Pdf2xml:
    def __init__(self, config_path):
        self.client = grobid.grobid_client(config_path=config_path)
        pass

    def process(self, work_dir, workers):
        input_dir = "cache/%s/pdfcache" % work_dir
        output_dir = "cache/%s/xmlcache" % work_dir
        self.client.process("processFulltextDocument", input_path=input_dir, output=output_dir, n=workers)

    def processTest(self, workers):
        self.client.process("processFulltextDocument", input_path="../cache/test/pdfcache", output="../cache/test/xmlcache", n=workers)


if __name__ == "__main__":
    pdf2xml = Pdf2xml("/home/vsphere/Workspace/grobid_client/grobid_client_python/config.json")
    pdf2xml.processTest(workers=4)
