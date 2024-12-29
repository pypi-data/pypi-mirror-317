import random
import torch
import re
from RFML.core.Results import ResultType
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.models.FNN.model import NeuralNet
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.models.FNN.nltk_utils import \
    bag_of_words, tokenize


class FNNBOT:
    intents = None

    def __init__(self, model: str, vector_db_path: str):
        self.model = model

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        FILE = fr"{vector_db_path}\{self.model}.pth"
        try:
            data = torch.load(FILE, weights_only=False)
        except Exception as e:
            print(str(e))
            return

        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        self.all_words = data['all_words']
        self.tags = data['tags']
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
        self.model.load_state_dict(model_state)
        self.model.eval()

    def predict(self, sentence: str, intents):
        _sentence = sentence
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]
        route = self.get_route(intents, tag)

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        default_msg = f"I’d love to help! Can you provide a bit more detail or rephrase your query?"
        if prob.item() > 0.95:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    # print(f"{bot_name}: {random.choice(intent['responses'])}")
                    if tag == "donation":
                        pattern = r"(Save\s*the\s*Children|SCI|SCiBD|SCIBD)"
                        matches = re.findall(pattern, _sentence, re.IGNORECASE)
                        if not matches:
                            return tag, route, default_msg, ResultType.do_not_understand
                    return tag, route, f"{random.choice(intent['responses'])}", ResultType.model_default
        else:
            # print(f"{bot_name}: I do not understand...")
            return \
                tag, route, \
                    default_msg, \
                    ResultType.do_not_understand

    def get_route(self, json_data, key):
        for item in json_data["intents"]:
            if item["tag"] == key:
                try:
                    return item["route"]
                except KeyError as ke:
                    return ""
