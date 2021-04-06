import spacy
import scispacy
import json

from typing import Union
from typing import Dict


class NER:
    def __init__(self, load_model=False):
        self.nlp = None

        if load_model:
            self.load_model()

    def load_model(self):
        self.nlp = spacy.load("en_ner_bionlp13cg_md")

    def predicte(self, text, simple_mode=True, return_dict=True) -> Union[str, Dict]:
        doc = self.nlp(text)
        doc_dict = doc.to_json()
        doc_json = json.dumps(doc_dict)

        if not doc_json:
            return json.dumps({"text": text})
        if not simple_mode:
            if return_dict:
                return doc_dict
            return doc_json

        simple_doc = dict([("text", doc_dict["text"]), ("ents", doc_dict["ents"])])
        if return_dict:
            return simple_doc
        simple_doc_json = json.dumps(simple_doc)
        return simple_doc_json


if __name__ == "__main__":
    ner = NER()
    ner.load_model()
    result = ner.predicte(
        "Moreover, the protective effect of the antioxidant NAC on monomer-induced MAPK activation and "
        "apoptosis suggested that MAPK activation was redoxsensitive but not the primary mechanism of "
        "monomer-induced apoptosis .Alternatively, we hypothesized that monomer-induced apoptosis may be "
        "initiated by the cellular response to oxidative DNA damage followed by the formation of DNA "
        "double-strand breaks (DSB).")
    print(result)
