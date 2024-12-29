from RFML.core.Conversation import Context
from RFML.core.Interaction import Interaction
from RFML.core.Results import PromptProcessResult
from RFML.core.SentenceFilters import SentenceFilters
from RFML.interface.IPromptValidator import IPromptValidator
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery
import re


class Validator(IPromptValidator):
    def configure_sentence_filter(self, filters: SentenceFilters, context: Context,
                                  interaction: Interaction) -> str:
        pass

    # configure prompt_queries for validation check
    def configure_prompt_queries(self, model_name: str, prompt_query_list: list[PromptQuery]):
        if model_name == "rf-ce-room_vehicle_booking":
            self.booking_validation(prompt_query_list)

    def booking_validation(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("action", {
                "Q1": "Could you specify what action do you prefer?",
                "Q2": "Please specify the action to perform"
            })
        )
        prompt_query_list.append(
            PromptQuery("room", {
                "Q1": "Could you specify the room name?",
                "Q2": "Please mention room name."
            })
        )
        prompt_query_list.append(
            PromptQuery("date", {
                "Q1": "Could you specify the date?",
                "Q2": "Please mention date."
            })
        )
        prompt_query_list.append(
            PromptQuery("start", {
                "Q1": "Could you specify the start time?",
                "Q2": "Please mention the the start time."
            })
        )
        prompt_query_list.append(
            PromptQuery("end", {
                "Q1": "Could you specify the end time?",
                "Q2": "Please mention the the end time"
            })
        )

    def rooom_booking(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("Room_ID", {
                "Q1": "Which room is your priority?",
                "Q2": "Please specify the room name"
            })
        )

        prompt_query_list.append(
            PromptQuery("Pickup_time", {
                "Q1": "From when the room will be needed?",
                "Q2": "Please specify the start time for room reservation"
            })
        )
        prompt_query_list.append(
            PromptQuery("Drop_time", {
                "Q1": "Until when the room will be needed?",
                "Q2": "Please specify the end time for room reservation"
            })
        )
        prompt_query_list.append(
            PromptQuery("Pickup_date", {
                "Q1": "Could you specify the room booking date?",
                "Q2": "Please specify the room booking date"
            })
        )
        prompt_query_list.append(
            PromptQuery("Participant", {
                "Q1": "How many participants will be attending?",
                "Q2": "Please specify the number of participants"
            })
        )
        prompt_query_list.append(
            PromptQuery("Meeting_purpose", {
                "Q1": "The room will be needed for which reason?",
                "Q2": "Please specify the purpose of room booking"
            })
        )

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str) -> PromptProcessResult:
        if model_name == "rf-ce-pr_process":
            if pc.missing_validator_attribute == "Time" and user_input != "today":
                return PromptProcessResult(False, "Please provide only (today) as date")
        # if pc: pc.validator_cash[pc.missing_validator_attribute] = user_input

    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str):
        import re
        if model_name == "rf-ce-room_vehicle_booking":
            msg = ""
            if valid_fields.get('action') == "show":
                if valid_fields.get('date'): msg = f"Show meeting rooms are free on {valid_fields['date']}"
                if valid_fields.get('start'): msg += f"from {valid_fields['start']} to "
                if valid_fields.get('end'): msg += f"{valid_fields['end']}."
            elif valid_fields.get('action') == "book":
                if valid_fields.get('room'): msg = f"Book the room {valid_fields['room']} from"
                if valid_fields.get('start'): msg = f"{valid_fields['start']} to "
                if valid_fields.get('end'): msg = f"{valid_fields['end']} on "
                if valid_fields.get('date'): msg = f"{valid_fields['date']} for "
                if valid_fields.get('pertinent'): msg = f"{valid_fields['pertinent']} for "
                if valid_fields.get('purpose'): msg = f"{valid_fields['purpose']}."
            elif valid_fields.get('action') == "cancel":
                # Cancel the meeting request number R548 scheduled for 8 AM in the Amazon room on 8th December.
                if valid_fields.get('request_no'):
                    msg = f"Cancel the meeting request number {valid_fields['request_no']}"
                if valid_fields.get('start'): msg += f"scheduled for {valid_fields['start']} in "
                if valid_fields.get('room'): msg += f"the {valid_fields['room']} room on "
                if valid_fields.get('date'): msg += f"{valid_fields['date']}."
            return msg
        elif model_name == "rf-ce-leave":
            msg = ""
            if valid_fields.get('Action') == "show":
                if valid_fields.get('Time'): msg = f"show me PRs to approve {valid_fields['Time']}"
            elif valid_fields.get('Action') == "approve":
                if valid_fields.get('PR'): msg = f"please approve the PR number {valid_fields['PR']}"
            elif valid_fields.get('Action') == "disapprove":
                if valid_fields.get('PR'): msg = f"Please disapprove PR number {valid_fields['PR']}"
            return msg

        # msg = ""
        # if valid_fields.get('Pickup_time'): msg += f"Please book a room from {valid_fields['Pickup_time']} to "
        # if valid_fields.get('Drop_time'): msg += f"{valid_fields['Drop_time']} on "
        # if valid_fields.get('Pickup_date'): msg += f"{valid_fields['Pickup_date']} at "
        # if valid_fields.get('Room_ID'): msg += f"{valid_fields['Room_ID']} for "
        # if valid_fields.get('Participant'): msg += f"{valid_fields['Participant']} participants for "
        # if valid_fields.get('Meeting_purpose'): msg += f"{valid_fields['Meeting_purpose']}."
        # result = re.sub(r"\b(at|on|to|for)\b$", "", msg.strip()).strip()
        # return result
