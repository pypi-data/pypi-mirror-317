import spacy
from RFML.core.Results import PredictResult, ResultType
from RFML.libs.utils import rf


class T2VModel:
    def __init__(self, model: str, vector_db_path: str):
        try:
            self.nlp = spacy.load(rf"{vector_db_path}\{model}\model-best")
        except Exception as e:
            print(e)

    def predict(self, input_text):
        doc = self.nlp(input_text)

        data = {
            "Room_ID": "", "Pickup_time": "", "Drop_time": "", "Pickup_date": "", "Participant": "",
            "Meeting_purpose": "", "Drop_date": "", "Pickup_point": "", "Destination": "", "Leave_initiate": "",
            "Leave_terminate": "", "Leave_type": "", "Leave_reason": "",

        }

        # valid, root = SentenceValidator().validate_sentence(self.nlp, input_text, ["room", "book"])
        if not self.valid_keywords(input_text):
            return PredictResult(
                result_type=ResultType.do_not_understand, label="room_booking",
                message="The booking details are not clearly specified!-Room Booking"
            )

        for ent in doc.ents:
            if ent.label_ in ["Room_ID", 'Pickup_point']:
                data[ent.label_] = ent.text
                if ent.label_ == 'Pickup_point': data['Room_ID'] = ent.text
            elif ent.label_ in ["Participant"]:
                participant_text = ent.text.lower()
                # Try converting using your function
                if participant_text.isdigit():
                    # If it's a digit, directly convert
                    data["Participant"] = participant_text
                else:
                    # Convert word number to digit
                    num = rf.number.convert_word_to_number(participant_text)
                    data["Participant"] = str(num)
            elif ent.label_ in ["Meeting_purpose", "Leave_reason"]:
                data["Meeting_purpose"] = ent.text
            else:
                data[ent.label_] = ent.text

        if len(doc.ents) > 0:
            return PredictResult(label="room_booking", message=data)
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand, label="room_booking",
                message="The booking details are not clearly specified!-Room Booking"
            )

    def valid_keywords(self, text):
        keywords1 = ["book", "reserve", "show"]
        keyword2 = "room"

        # Check if any word from keywords1 and keyword2 are in the text
        if any(word in text.lower() for word in keywords1) and keyword2 in text.lower():
            return True
        return False
