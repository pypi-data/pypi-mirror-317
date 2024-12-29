from RFML.core.ModelCache import ModelCache
from RFML.core.Results import GenerateResult
from RFML.engines.supervised.NLP.information_extraction.command_extractor.corpus.CommandExtractionCorpus import \
    CommandExtractionCorpus
from RFML.interface.ITrainingCorpus import ITrainingCorpus
from RFML.interface.IGenerate import IGenerate, T
from bson import json_util

from RFML.libs.utils import rf


class Generator(IGenerate[CommandExtractionCorpus]):
    def __init__(self, model, vector_db_home: str):
        self.model = model
        self.vector_db_home = vector_db_home

    def before_generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus):
        pass

    def generate(self, model_name: str, training_corpus: CommandExtractionCorpus,
                 corpus: ITrainingCorpus, gen_info) -> GenerateResult:

        msg = ""
        if gen_info['command'] == 'split':
            # dataset = corpus.cognitive.read({"model": model_name})['ner']
            msg = rf.gen.split_data(self.vector_db_home, model_name, gen_info["index"])
        elif gen_info['command'] == 'make':
            msg = rf.gen.make_file(gen_info["make_type"], self.vector_db_home, model_name)
        elif gen_info['command'] == 'split_make':
            # dataset = corpus.cognitive.read({"model": model_name})['ner']
            ret1 = rf.gen.split_data(self.vector_db_home, model_name, gen_info["make_type_index"])
            ret2 = rf.gen.make_file('spacy', self.vector_db_home, model_name)
            msg = msg + " " + ret1 + " " + ret2
        elif gen_info['command'] == 'entity':
            data = corpus.training.read({"model": model_name})['ner']
            msg = rf.gen.generate_entity_data(data, self.vector_db_home, model_name)
        elif gen_info['command'] == 'all':
            data = corpus.training.read({"model": model_name})['ner']
            msg = rf.gen.generate_entity_data(data, self.vector_db_home, model_name)
            ret1 = rf.gen.split_data(self.vector_db_home, model_name, gen_info["make_type_index"])
            ret2 = rf.gen.make_file('spacy', self.vector_db_home, model_name)
            msg = msg + " " + ret1 + " " + ret2

        return GenerateResult(message=msg)

    def after_generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus):
        pass
