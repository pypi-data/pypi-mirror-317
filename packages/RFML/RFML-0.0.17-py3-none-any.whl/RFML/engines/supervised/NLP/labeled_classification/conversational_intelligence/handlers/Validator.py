from nltk.parse.transitionparser import Configuration
from spacy.pipeline.spancat import preset_spans_suggester

from RFML.core.Conversation import Context
from RFML.core.Interaction import Interaction
from RFML.core.SentenceFilters import SentenceFilters
from RFML.core.SentenceFilterConfiguration import SentenceFilterConfiguration
from RFML.interface.IPromptValidator import IPromptValidator
from RFML.interface.ISentenceFilter import ISentenceFilter
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery

import spacy
from spacy.matcher import Matcher


class Validator(IPromptValidator):
    nlp = spacy.load("en_core_web_sm")

    def __init__(self):
        # Load the spaCy language model
        # Initialize the Matcher
        self.matcher = Matcher(self.nlp.vocab)

    # configure prompt_queries for validation check
    def configure_prompt_queries(self, model_name: str, prompt_query_list: list[PromptQuery]):
        pass

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str):
        pass

    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str) -> str:
        pass

    def configure_sentence_filter(self, filters: SentenceFilters, context: Context,
                                  interaction: Interaction) -> str:
        filters.allow_one_word_patterns(["Hi", "Hello", "Hey", "Greetings", "Thanks", "Good Bye"])
        filters.block_invalid_sentences(
            ["can do", "what can do", "donate how", "how donate"]
        )
        filters.allow_multi_word_patterns(SCIDonorFilter(), ["donate", "contribute"])
        pass


class SCIDonorFilter(ISentenceFilter):
    def configure(self, configuration: SentenceFilterConfiguration):
        configuration.set_patterns([
            {"LOWER": {"REGEX": "(how|what|can|ways|guide)"}, "IS_SENT_START": True},  # Question starters
            {"LEMMA": "to", "OP": "?"},
            {"LEMMA": {"REGEX": "(donate|contribute|send|make)"}},  # Synonyms for "donate"
            {"TEXT": {"REGEX": "(donation|donations)?"}, "OP": "?"},
            {"LOWER": {"REGEX": "(in|to|for)"}, "OP": "?"},  # Prepositions
            {"LOWER": {"REGEX": "(save|children|the)"}, "OP": "+"},  # Matches "Save the Children"
            {"TEXT": "?", "OP": "?"}  # Optional question mark
        ])
        configuration.set_rules.has_verb(["donate", "contribute", "send"])
        # configuration.set_rules.has_preposition(["to"])
