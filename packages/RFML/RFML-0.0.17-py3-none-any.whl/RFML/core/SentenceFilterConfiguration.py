import uuid

import spacy
from spacy.matcher import Matcher


class Rules:
    verbs = []
    preps = []
    all = [verbs, preps]

    def has_verb(self, verbs):
        self.verbs = verbs

    def has_preposition(self, preps):
        self.preps = preps


class SentenceFilterConfiguration:
    default_message = "Could you provide additional details, please?"
    set_rules = Rules()

    nlp = spacy.load("en_core_web_sm")

    def __init__(self):
        self.matcher = Matcher(self.nlp.vocab)

    def add_default_message(self, message="Could you provide additional details, please?"):
        self.default_message = message

    def set_patterns(self, patterns: []):
        _uuid = str(uuid.uuid4()).replace('-', '')
        self.matcher.add(_uuid, [patterns])
