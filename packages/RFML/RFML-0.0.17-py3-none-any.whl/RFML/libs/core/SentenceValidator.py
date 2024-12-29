from RFML.core.Interaction import Interaction
from RFML.core.SentenceFilterConfiguration import SentenceFilterConfiguration
from RFML.core.SentenceFilters import SentenceFilters


class SentenceValidator:

    def validate_sentence(self, tool, sentence: str, expected_keywords=None) -> (bool, str):
        matches = tool.check(sentence[0].upper() + sentence[1:])
        if matches:
            errors = []
            for match in matches: errors.append("spell" if "spell" in match.message else "others")
            if len(errors) == 1 and errors[0] == "spell": return True, ""
        return (True, "") if not matches else (False, "")

    def validate_sentence1(self, nlp, sentence: str, expected_keywords=None) -> (bool, str):
        """
        Validate if the input sentence is grammatically structured and contextually relevant.

        Args:
        - sentence (str): The user-input sentence to validate.
        - expected_keywords (list, optional): List of keywords to check for context validity.

        Returns:
        - str: Validation feedback.
        """
        # Parse the sentence
        doc = nlp(sentence)

        # Validate verb,adverb positioning
        root_lemma, adverb, verb = "", None, None
        for token in doc:
            if token.dep_ == "ROOT":
                root_lemma = token.lemma_
            # print(token.pos_)
            if token.pos_ == "ADV" or token.pos_ == "INTJ":  # Check if the token is an adverb
                adverb = token
            elif token.pos_ == "VERB":  # Check if the token is a verb
                verb = token

        # Check if the sentence contains a ROOT (main verb or clause)
        if not any(token.dep_ == "ROOT" for token in doc):
            return False, root_lemma  # f"{sentence} -- Invalid sentence: No main verb or clause (ROOT) detected."

        # Check for proper noun-verb relationships
        has_subject = True  # any(token.dep_ in ("nsubj", "nsubjpass") for token in doc)
        has_verb = any(token.pos_ == "VERB" for token in doc)
        if not (has_subject and has_verb):
            return False, root_lemma  # f"{sentence} -- Invalid sentence: Missing a subject or verb."

        # Validate against expected keywords for context relevance
        if expected_keywords:
            if not any(keyword.lower() in sentence.lower() for keyword in expected_keywords):
                return False, root_lemma  # f"{sentence} -- Invalid sentence: Does not match the expected context (missing keywords: {', '.join(expected_keywords)})."

        # Check for completeness (length or punctuation, e.g., question mark for questions)
        if len(sentence.split()) < 3:  # Arbitrary threshold for completeness
            return False, root_lemma  # "Invalid sentence: Too short or incomplete."

        # Validate verb,adverb positioning
        if adverb and verb:
            if adverb.i < verb.i:
                return True, root_lemma  # print(f"The adverb '{adverb.text}' is correctly positioned before the verb '{verb.text}'.")
            else:
                return False, root_lemma  # print(f"The adverb '{adverb.text}' is incorrectly positioned after the verb '{verb.text}'.")
        # else:
        #     return False, root_lemma  # print("No adverb or verb found in the sentence.")

        return True, root_lemma  # f"{sentence} -- Valid sentence: Grammatically correct and contextually relevant."

    def is_valid_pattern(self, _filter: SentenceFilters, interaction: Interaction, root_lemma) -> bool:
        found = next((key for key, value in _filter.multi_word_lemmas.items()
                      if isinstance(value, list) and root_lemma in value), None)
        pattern = _filter.multi_word_patterns.get(found)
        if pattern:
            if not _filter.multi_word_enabled[found]: return True
            config = SentenceFilterConfiguration()
            pattern.configure(config)
            doc = config.nlp(interaction.input)
            matches = config.matcher(doc)

            if not matches: return False
            for token in doc:
                if config.set_rules.verbs:
                    if token.dep_ == "ROOT" and token.lemma_ not in config.set_rules.verbs: return False
                if config.set_rules.preps:  # allowing preposition for now
                    if token.dep_ == "prep" and token.text not in config.set_rules.preps: return False
            return True
        return True

        # for pattern in _filter.multi_word_pattern_objects:
        #
        #     if any(lemma in root_lemma for lemma in pattern.root_lemmas):
        #         if not pattern.multi_word_enabled: return True
        #         config = SentenceFilterConfiguration()
        #         pattern.multi_word_patterns.configure(config)
        #         # ret = self.is_correct_pattern(config.nlp, config.matcher, interaction.input)
        #         doc = config.nlp(interaction.input)
        #         matches = config.matcher(doc)
        #
        #         if not matches: return False
        #         for token in doc:
        #             if config.set_rules.verbs:
        #                 if token.dep_ == "ROOT" and token.lemma_ not in config.set_rules.verbs: return False
        #             if config.set_rules.preps:  # allowing preposition for now
        #                 if token.dep_ == "prep" and token.text not in config.set_rules.preps: return False
        #         return True
        # return True

    def is_correct_text(self, _config, user_input) -> (bool, str):
        doc = _config.nlp(user_input)
        root_lama, new_sentence = "", ""

        for token in doc:
            if token.dep_ == "ROOT": root_lama = token.lemma_
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                # Check if the sentence lacks an explicit subject
                _subject = any(child.dep_ in ("nsubj", "nsubjpass") for child in token.children)
                if not _subject: new_sentence = "You " + user_input  # Implicit subject in imperatives

        doc = _config.nlp(new_sentence or user_input)
        # Check if the sentence contains a root verb and subject
        has_root = any(token.dep_ == "ROOT" for token in doc)
        has_subject = any(token.dep_ in ("nsubj", "nsubjpass") for token in doc)

        # Simple logic to flag incomplete sentences
        return (True, root_lama) if has_root and has_subject else (False, root_lama)

        # root_lama = ""
        # subject, verb = None, None
        # token_count = 0
        # for token in doc:
        #     if "ROOT" in token.dep_: root_lama = token.lemma_
        #     if 'subj' in token.dep_:
        #         subject = token
        #     elif 'VERB' in token.pos_:
        #         verb = token
        #         if token_count == 0: subject = "You "  # implied subject
        #         token_count = token_count + 1
        # return bool(subject and verb), root_lama
