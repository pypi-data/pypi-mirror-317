import uuid

from RFML.interface.ISentenceFilter import ISentenceFilter


class SentenceFilters:
    one_word_patterns = []
    block_sentences_patterns = []
    match_invalid_patterns = []

    multi_word_patterns = {}
    multi_word_lemmas = {}
    multi_word_enabled = {}

    def allow_multi_word_patterns(self, sentence_filter: ISentenceFilter, root_lemmas, enabled=True):
        # auto name model_name+label+lemma
        uid = str(uuid.uuid4()).replace('-', '')
        self.multi_word_lemmas[uid] = root_lemmas
        self.multi_word_patterns[uid] = sentence_filter
        self.multi_word_enabled[uid] = enabled

    def allow_one_word_patterns(self, one_words: []):
        for item in one_words:
            if item not in self.one_word_patterns: self.one_word_patterns.append(item)
        # if one_words: self.one_word_patterns.extend(one_words)

    def block_invalid_sentences(self, block_sentences: []):
        for item in block_sentences:
            if item not in self.block_sentences_patterns:
                self.block_sentences_patterns.append(item)
                self.match_invalid_patterns.clear()
                for pattern in self.block_sentences_patterns:
                    words = []
                    for word in pattern.split():
                        words.append({"LOWER": word})

                    self.match_invalid_patterns.append(words)
        # if block_sentences: self.block_sentences_patterns.extend(block_sentences)
