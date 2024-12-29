import spacy
from RFML.core.Results import PredictResult, ResultType
from RFML.libs.utils import rf


class T2VModelNew:
    def __init__(self, model: str, vector_db_path: str):
        try:
            self.nlp = spacy.load(rf"{vector_db_path}\{model}\model-best")
        except Exception as e:
            print(e)

    def predict(self, model_name, sentence):
        if model_name == "rf-ce-room_vehicle_booking":
            return self.predict_booking(sentence)

    def predict_booking(self, sentence):
        data = {}
        action = ""
        data_show = {"action": "", "date": "", "start": ""}
        data_book = {"action": "", "room": "", "date": "", "start": "", "end": "", "percipient": "", "purpose": ""}
        data_cancel = {"action": "", "request_no": "", "room": "", "date": "", "start": ""}

        if not self.valid_keywords(sentence):
            return PredictResult(
                result_type=ResultType.do_not_understand, label="room_booking",
                message="The booking details are not clearly specified!-Room Booking"
            )

        doc = self.nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "action":
                action = ent.text.lower()  # "Entity:ent.text, Label:ent.label_"
            data[ent.label_] = ent.text

        if not action:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="pr_booking",
                message="The booking [action] are not clearly specified!"
            )

        action_data = {"show": data_show, "book": data_book, "cancel": data_cancel}
        action_data[action].update(data)

        if len(doc.ents) > 0 and (action in ["show", "cancel", "book"]) and \
                any(keyword in sentence for keyword in ["room"]):
            return PredictResult(label="pr_booking", message=action_data[action])
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="pr_booking",
                message="The booking details are not clearly specified!"
            )

    def valid_keywords(self, text):
        keywords1 = ["cancel", "book", "reserve", "show"]
        keyword2 = "room"

        # Check if any word from keywords1 and keyword2 are in the text
        if any(word in text.lower() for word in keywords1) and keyword2 in text.lower():
            return True
        return False
