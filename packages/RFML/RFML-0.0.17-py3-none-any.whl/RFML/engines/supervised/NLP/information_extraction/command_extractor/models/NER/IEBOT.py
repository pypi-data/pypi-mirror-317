import spacy
from RFML.core.Results import PredictResult, ResultType


class IEBOT:
    def __init__(self, model: str, vector_db_path: str):
        try:
            self.nlp = spacy.load(rf"{vector_db_path}\{model}")
        except Exception as e:
            print(e)

    def predict(self, model_name: str, sentence: str):
        if model_name == "rf-ce-flight_booking":
            return self.predict_flight(sentence)
        elif model_name == "rf-ce-pr_process":
            return self.predict_pr(sentence)
        elif model_name == "rf-ce-room_vehicle_booking":
            return self.predict_booking(sentence)

    def predict_pr(self, sentence: str):
        data = {}
        action = ""
        data_show = {"Action": "", "Time": ""}
        data_approve = {"Action": "", "PR": ""}

        doc = self.nlp(sentence)
        for ent in doc.ents:
            if ent.label_ == "Action": action = ent.text.lower()  # "Entity:ent.text, Label:ent.label_"
            data[ent.label_] = ent.text

        (data_show if action == "show" else data_approve).update(data)

        if len(doc.ents) > 0 and (action == "show" or action == "approve" or action == "disapprove") and \
                any(keyword in sentence for keyword in ["PR", "PRs"]):
            return PredictResult(label="pr_booking", message=data_show if action == "show" else data_approve)
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="pr_booking",
                message="The PR details are not clearly specified!"
            )

    def predict_flight(self, sentence: str):
        doc = self.nlp(sentence)
        data = {
            "Action": "",
            "Origin": "",
            "Destination": "",
            "Date": "",
            "Time": ""
        }
        for ent in doc.ents: data[ent.label_] = ent.text  # "Entity:ent.text, Label:ent.label_

        if len(doc.ents) > 0 and data["Action"] == "book" and "flight" in sentence:
            return PredictResult(label="flight_booking", message=data)
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="flight_booking",
                message="The booking details are not clearly specified! - Flight Booking"
            )

    commands_show = ["show", "display", "view", "explore", "browse"]
    commands_book = ["book", "reserve", "schedule", "manage", "arrange"]
    commands_cancel = ["cancel", "abort", "remove", "stop"]
    commands = commands_show + commands_book + commands_cancel

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
            if ent.label_ == "action": action = ent.text.lower()
            data[ent.label_] = ent.text

        if not action:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="pr_booking",
                message="The booking [action] are not clearly specified!"
            )

        action_data = {"show": data_show, "book": data_book, "cancel": data_cancel}
        action_data[self.command_key(action)].update(data)

        if len(doc.ents) > 0:
            return PredictResult(label="pr_booking", message=action_data[self.command_key(action)])
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="pr_booking",
                message="The booking details are not clearly specified!"
            )

    def valid_keywords(self, text):
        keywords1, keyword2 = self.commands, "room"
        if any(word in text.lower() for word in keywords1) and keyword2 in text.lower(): return True
        return False

    def command_key(self, word):
        if word.lower() in self.commands_show: return "show"
        if word.lower() in self.commands_book: return "book"
        if word.lower() in self.commands_cancel: return "cancel"
