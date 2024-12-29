from RFML.core.ModelCache import ModelCache
from RFML.core.Results import GenerateResult
from RFML.engines.supervised.NLP.information_extraction.command_extractor.corpus.CommandExtractionCorpus import \
    CommandExtractionCorpus
from RFML.interface.ITrainingCorpus import ITrainingCorpus
from RFML.interface.IGenerate import IGenerate, T
from RFML.libs.utils import rf


class Generator(IGenerate[CommandExtractionCorpus]):
    def __init__(self, model, vector_db_home: str):
        self.model = model
        self.vector_db_home = vector_db_home

    def before_generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus):
        pass

    def generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus,
                 gen_info) -> GenerateResult:
        return GenerateResult("", "")

    def after_generate(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: ITrainingCorpus):
        pass
