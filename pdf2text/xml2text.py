from lxml import etree

import os
import json

from typing import Optional
from typing import List
from typing import Dict
from typing import Union


class Xml2text:
    def __init__(self):
        self.articles = []

    def parse_xml_dir(self, dir_in):
        paths = os.listdir(dir_in)
        for file in paths:
            sp_name = os.path.splitext(file)
            if sp_name[1] == ".xml":
                file_in = os.path.join(dir_in, file)
                self.parse_xml(file_in)

    def parse_xml(self, path_in):
        with open(path_in, "rb") as fr:
            xml_str = fr.read()
            parse_result = self.parse_test2(xml_str)

            self.articles.append(parse_result)

    def parse_test2(self, xml_str: Union[str, bytes]) -> Dict:
        result_dict = {"title": None, "abstract": None, "body": None}
        # xml_str = open("test/1.o.xml", "rb").read()
        # xml_str = file_reader.read()
        xml = etree.XML(xml_str)
        ns = self.get_namespace(xml)

        title = self.parse_text(xml, "//default:title/text()", ns)
        if title:
            result_dict["title"] = str(title[0])
            # write_result(file_writer, "TITLE", str(title[0]))
        # print(title)

        abstract = self.parse_text(xml, "//default:abstract//default:p/text()", ns)
        if abstract:
            result_dict["abstract"] = str(abstract[0])
            # write_result(file_writer, "ABSTRACT", str(abstract[0]))
        # print(abstract)

        parps = self.parse_text(xml, "//default:body/default:div", ns)
        # print(parps)

        body = []
        for i, parp in enumerate(parps):
            head = self.parse_text(parp, "./default:head/text()", ns)
            tag_ps = self.parse_text(parp, "./default:p", ns)
            text_total = self.get_text(tag_ps, ns)
            body.append({"heads": head, "texts": text_total})

        result_dict["body"] = body
        # write_result(file_writer, "BODY", body)

        return result_dict

    def parse_text(self, root_node, regex, namespaces) -> Optional[List[str]]:
        text = root_node.xpath(regex, namespaces=namespaces)
        if text is None or len(text) == 0:
            return None
        return text

    def get_namespace(self, root_node):
        namespace = root_node[0].nsmap
        for node in root_node:
            for key, value in node.nsmap.items():
                namespace[key] = value
        namespace["default"] = namespace[None]
        namespace.pop(None)
        return namespace

    def get_text(self, tag_ps: list, namespaces) -> List[str]:
        text_total = []

        if tag_ps is None or len(tag_ps) == 0:
            return text_total

        for tag_p in tag_ps:
            text_str = "".join(self.collect_text(tag_p, namespaces))
            text_total.append(text_str)

        return text_total

    def collect_text(self, tag_p, namespaces) -> List[str]:
        tag_refs: list = self.parse_text(tag_p, "./default:ref", namespaces)
        text_list = []

        if tag_refs is None or len(tag_refs) == 0:
            text_list: list = self.parse_text(tag_p, "./text()", namespaces)
            return text_list

        tag_ref = tag_refs[0]
        for item in tag_p.iter():
            if item.tag == tag_ref.tag:
                text = item.tail
            else:
                text = item.text
            if text:
                text_list.append(text)

        return text_list

    def clear_articles(self):
        self.articles = []


if __name__ == "__main__":
    xml2text = Xml2text()
    xml2text.parse_xml_dir("../cache/test/xmlcache")
    xml2text.parse_xml_dir("../cache/test/xmlcache")
    print("done")
