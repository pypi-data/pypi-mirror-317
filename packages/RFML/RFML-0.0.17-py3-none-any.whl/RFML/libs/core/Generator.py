from os import mkdir
from pathlib import Path
from bson import json_util
import spacy
from spacy.training import Example
from spacy.tokens import DocBin
import json
import random

from RFML.libs.NLP.NERGen import ExtractionCorpus, Entity, CorpusData, NEREntityMismatchError


class Generator:
    def __mkdir(self, vector_db_home, model_name):
        path = f"{vector_db_home}\\{model_name}\\corpus"
        directory_path = Path(path)
        directory_path.mkdir(parents=True, exist_ok=True)
        return path

    def split_data(self, vector_db_home, model_name, index=0.8):
        path = self.__mkdir(vector_db_home, model_name)
        # json_data = json.dumps(corpus, default=json_util.default)
        # with open(f"{path}\\data.json", "w") as file: file.write(json_data)
        data_json_path = f"{path}\\data.json"

        return self.__split(data_json_path, vector_db_home, model_name, index)

    def make_file(self, json_file, vector_db_home, model_name):
        return self.__make(json_file, vector_db_home, model_name)

    def __split(self, json_file, vector_db_home, model_name, index=0.8):

        # Step 1: Load JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Step 2: Shuffle the data
        random.shuffle(data)

        # Step 3: Split the data into training and development sets
        split_index = int(len(data) * 0.8)
        train_data = data[:split_index]
        dev_data = data[split_index:]

        path = self.__mkdir(vector_db_home, model_name)
        # Step 4: Save the datasets to separate JSON files
        with open(f'{path}\\train.json', 'w') as f:
            json.dump(train_data, f, indent=2)

        with open(f'{path}\\dev.json', 'w') as f:
            json.dump(dev_data, f, indent=2)

        return f"Data has been split into {len(train_data)} training samples and {len(dev_data)} development samples."

    def __make(self, json_file, vector_db_home, model_name):
        path = self.__mkdir(vector_db_home, model_name)
        for item in ["train", "dev"]:
            # Step 1: Load JSON data
            with open(f'{path}\\data.json', 'r') as f:
                data = json.load(f)

            # Step 2: Convert JSON to spaCy training format
            def create_examples(data):
                examples = []
                for item in data:
                    text = item['text']
                    entities = [(e['start'], e['end'], e['label']) for e in item['entities']]
                    examples.append((text, {"entities": entities}))
                return examples

            def save_spacy_format(examples, output_file):
                nlp = spacy.blank("en")  # Create a blank English model
                doc_bin = DocBin()  # Create a DocBin object to store the data

                for text, annot in examples:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, annot)
                    doc_bin.add(example.reference)

                doc_bin.to_disk(output_file)  # Save to .spacy format

            # Convert to spaCy training format
            examples = create_examples(data)

            # Save as .spacy file
            save_spacy_format(examples, f'{path}\\{item}.spacy')

        return f"Spacy binary files has been created!"

    __dataset_list = []

    def generate_entity_data(self, json_data, vector_db_home, model_name):
        text, index = "", 0
        try:
            for item in json_data:
                text = item['text']
                ner_map = item['ner_map']
                entity_list = []
                for key, value in ner_map.items():
                    entity_list.append(Entity(value, key))
                self.add(CorpusData(text, entity_list))
                index = index + 1

            path = self.__mkdir(vector_db_home, model_name)
            with open(f'{path}\\data.json', 'w') as f:
                json.dump(self.__dataset_list, f, indent=2)

            return "Entity json data generation was successful!"

        except NEREntityMismatchError as e:
            msg = f"This text '{text}' has some entity mismatch at row index: {index}. Data generation is failed!"
            return None, msg

    def add(self, dataset: CorpusData):
        entity_map_list = []
        for item in dataset.entities:
            entity_map = {"entity": item.entity, "label": item.label}
            entity_map_list.append(entity_map)
        _entities = self.__generate_data(dataset.text, entity_map_list)
        ner = {"text": dataset.text, "entities": _entities}
        self.__dataset_list.append(ner)

    def __generate_data(self, text, entities):
        pos_list = []
        for entity in entities:
            entity_text = entity["entity"]
            start_pos = text.find(entity_text)
            if start_pos != -1:
                end_pos = start_pos + len(entity_text)
                pos_list.append({"start": start_pos, "end": end_pos, "label": entity['label']})
            else:
                try:
                    var = end_pos
                except Exception as e:
                    raise NEREntityMismatchError("Entity mismatch for the given text.")
        return pos_list
