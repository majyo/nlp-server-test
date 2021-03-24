from nerModule import NER
import tornado.web
import tornado.ioloop
import json


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # self.set_header('Access-Control-Max-Age', 1000)


class MainHandler(BaseHandler):
    def get(self):
        self.write("<p>This is a demonstration of the nlp platform.<p>")
        self.write("<p>To use this demo, please send JSON data to /api/allennlp/ner through POST request.<p>")


class NerHandler(BaseHandler):
    def initialize(self, ner):
        self.ner: NER = ner

    def prepare(self):
        if self.request.method == "GET":
            self.json_args = None
            return

        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = self.request.body
            return
        self.json_args = None

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


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler), (r"/api/allennlp/ner", NerHandler, dict(ner=start_ner_module())),
    ])


def start_ner_module():
    ner_instance = NER()
    ner_instance.load_model()
    return ner_instance


if __name__ == "__main__":
    app = make_app()
    app.listen(8001)
    print("Starting App...")
    tornado.ioloop.IOLoop.current().start()
