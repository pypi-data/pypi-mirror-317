from RFML.api.ServiceApi import ServiceApi
from RFML.core.ModelCache import ModelCache
from RFML.core.Results import PredictResult
from RFML.corpus.Corpus import Corpus
from RFML.engines.supervised.NLP.information_extraction.command_extractor_tok2vec.models.T2VModelNew import T2VModelNew
from RFML.interface.IPredict import IPredict


class Predictor(IPredict):
    def __init__(self, model, mc: ModelCache, vector_db_home: str):
        self.mc = mc
        self.bot = self.mc.get(model) or T2VModelNew(model, vector_db_home)
        if not self.mc.get(model): self.mc.load(model, self.bot)

    def reload_model(self, model_name: str, corpus: Corpus) -> str:  # MC issue xx import ??
        pass

    def before_predict(self, model_name: str, input_text: str) -> str:
        pass

    def predict(self, model_name: str, input_text: str, corpus: Corpus) -> PredictResult:
        result = self.bot.predict(model_name, input_text)
        return result

        # result = T2VModelNew(model_name, corpus.vector_db_home).predict(input_text)
        # return result

    def after_predict(self, model_name: str, predict_result: PredictResult, service_api: ServiceApi) -> PredictResult:
        return predict_result

    def on_model_callback(self, predict_result: PredictResult) -> PredictResult:
        pass
