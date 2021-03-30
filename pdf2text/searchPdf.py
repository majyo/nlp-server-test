from smb.SMBConnection import SMBConnection
import urllib.parse
import urllib.request
import re
import IPy

from typing import Dict


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
        self.url = "%s:%s/%s" % (host, port, path)

    def fetch(self, title: str, limit: int):
        query_path = urllib.parse.urlencode({"title": title, "limit": limit})
        query_url = "%s?%s" % (self.url, query_path)
        # print(query_url)


if __name__ == "__main__":
    searcher = PdfSearcher("192.168.40.10", "8001", "searchpdf")
    searcher.fetch("The properties of graphene", 2)
    with urllib.request.urlopen("192.168.40.10:8001/searchpdf?title=The+properties+of+graphene&limit=2") as f:
        data = f.read().decode("utf-8")
        print(data)
