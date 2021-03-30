import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument("title") and self.get_argument("limit"):
            self.set_status(200)
            self.set_header("Content-Type", "application/json")
            self.write("""
            {
    "ArticleList": [
        {
            "title": "Properties of graphene: a theoretical perspective",
            "authors": "Abergel,V. Apalkov,J. Berashevich,K. Ziegler",
            "journal": "Advances in Physics",
            "year": "2010",
            "smb": "smb://xxx.xxx.xxx.xxx"
        },
        {
            "title": "The electronic properties of graphene",
            "authors": "A. H. Castro Neto, F. Guinea, N. M. R. Peres, K. S. Novoselov, and A. K. Geim",
            "journal": "REVIEWS OF MODERN PHYSICS",
            "year": "2009",
            "smb": "smb://xxx.xxx.xxx.xxx"
        }
    ]
}
            """)


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/searchpdf", MainHandler),
    ])
    application.listen(7001)
    tornado.ioloop.IOLoop.current().start()
