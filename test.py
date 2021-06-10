if __name__ == "__main__":
    # lb = start_labeling_module()
    # uuid = lb.create_cache_dir()
    # print(uuid)
    # pdf_downloader = PdfDownloader()
    # pdf_downloader.get_pdf("smb://192.168.40.10/article/Influence%20of%20Host\u2013Guest%20Interaction%20between%20Chiral%20Selectors%20and%20Probes%20on%20the%20Enantioseparation%20Properties%20of%20Graphene%20Oxide%20Membranes.pdf", uuid)
    #
    # pdf2xml = Pdf2xml("/home/vsphere/Workspace/grobid_client/grobid_client_python/config.json")
    # pdf2xml.process(uuid, workers=4)
    #
    # xml2text = Xml2text()
    # xml2text.parse_xml_dir("cache/%s/xmlcache" % uuid)
    # print(json.dumps(xml2text.articles[0]))
    # lb.clear_cache_dir(uuid)
    # print(dict(a="haha"))
    # connection = SMBConnection("robin", "smb@123", "", "", use_ntlm_v2=True)
    # result = connection.connect("192.168.40.10", 445)
    # logging.info(result)
    a = [0.56, 0.754]
    a = a.index(max(a))
    print(a)
