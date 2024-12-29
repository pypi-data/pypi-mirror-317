from RFML.libs.NLP.NERGen import ExtractionCorpus, Entity, CorpusData, NEREntityMismatchError


class NERGenerator:
    def generate_fnn_data(self, json_data):
        text, index = "", 0
        try:
            corpus = ExtractionCorpus()
            for item in json_data['ner']:
                text = item['text']
                ner_map = item['ner_map']
                entity_list = []
                for key, value in ner_map.items():
                    entity_list.append(Entity(value, key))
                corpus.add(CorpusData(text, entity_list))
                index = index + 1
            return corpus.get(), ""

        except NEREntityMismatchError as e:
            msg = f"This text '{text}' has some entity mismatch at row index: {index}. Data generation is failed!"
            return None, msg
