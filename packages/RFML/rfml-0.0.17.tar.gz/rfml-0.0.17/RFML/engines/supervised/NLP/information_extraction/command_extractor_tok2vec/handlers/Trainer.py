from RFML.core.Results import TrainResult
from RFML.corpus.Corpus import Corpus
from RFML.engines.supervised.NLP.information_extraction.command_extractor.corpus.CommandExtractionCorpus import \
    CommandExtractionCorpus
from RFML.engines.supervised.NLP.information_extraction.command_extractor.models.NER.IEBOTTrainer import IEBOTTrainer
from RFML.engines.supervised.NLP.information_extraction.command_extractor_tok2vec.models.T2VModelTrainer import \
    T2VModelTrainer
from RFML.interface.ITrain import ITrain
from RFML.libs.utils import rf


class Trainer(ITrain[CommandExtractionCorpus]):
    def __init__(self, model, vector_db_home: str):
        self.model = model
        self.vector_db_home = vector_db_home

    def before_train(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: Corpus) -> TrainResult:
        return TrainResult("ss", 1, 1)

    def train(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: Corpus) -> TrainResult:
        # data_gen = corpus.training.read({"model": model_name})
        result = T2VModelTrainer.train(model_name, self.vector_db_home)

        return TrainResult(message=result)

    def after_train(self, model_name: str, training_corpus: CommandExtractionCorpus, corpus: Corpus) -> TrainResult:
        return TrainResult("ss", 1, 1)
