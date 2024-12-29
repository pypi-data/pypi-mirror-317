from RFML.core.Conversation import Context
from RFML.core.Interaction import Interaction
from RFML.core.Results import PromptProcessResult
from RFML.core.SentenceFilters import SentenceFilters
from RFML.interface.IPromptValidator import IPromptValidator
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery


class Validator(IPromptValidator):
    # configure prompt_queries for validation check
    def configure_prompt_queries(self, model_name: str, prompt_query_list: list[PromptQuery]):
        if model_name == "rf-ce-flight_booking":
            self.flight_validation(prompt_query_list)
        elif model_name == "rf-ce-pr_process":
            self.pr_validation(prompt_query_list)
        elif model_name == "rf-ce-room_vehicle_booking":
            self.booking_validation(prompt_query_list)

    def pr_validation(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("Action", {
                "Q1": "Could you specify PR action type?",
                "Q2": "Please specify the PR action"
            })
        )
        # show
        prompt_query_list.append(
            PromptQuery("Time", {
                "Q1": "Could you specify the time?",
                "Q2": "Please mention time."
            })
        )
        # approve
        prompt_query_list.append(
            PromptQuery("PR", {
                "Q1": "Could you specify the PR no?",
                "Q2": "Please mention PR no."
            })
        )

    def flight_validation(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("Action", {
                "Q1": "Could you specify the transport type?",
                "Q2": "Please specify the transport"
            })
        )
        prompt_query_list.append(
            PromptQuery("Origin", {
                "Q1": "Could you specify the source location?",
                "Q2": "Please mention source location."
            })
        )
        prompt_query_list.append(
            PromptQuery("Destination", {
                "Q1": "Could you specify the destination location?",
                "Q2": "Please mention destination location."
            })
        )
        prompt_query_list.append(
            PromptQuery("Date", {
                "Q1": "Could you specify the journey date?",
                "Q2": "Please mention the the journey date."
            })
        )
        prompt_query_list.append(
            PromptQuery("Time", {
                "Q1": "Could you specify the journey time...?",
                "Q2": "Please mention the the journey time..."
            })
        )

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

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str) -> PromptProcessResult:
        if model_name == "rf-ce-pr_process":
            if pc.missing_validator_attribute == "Time" and user_input != "today":
                return PromptProcessResult(False, "Please provide only (today) as date")
        # if pc: pc.validator_cash[pc.missing_validator_attribute] = user_input

    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str):
        import re
        if model_name == "rf-ce-flight_booking":
            msg = ""
            if valid_fields.get('Origin'): msg += f"Please book a flight from {valid_fields['Origin']} to "
            if valid_fields.get('Destination'): msg += f"{valid_fields['Destination']} on "
            if valid_fields.get('Date'): msg += f"{valid_fields['Date']} at "
            if valid_fields.get('Time'): msg += f"{valid_fields['Time']}."
            result = re.sub(r"\b(at|on|to)\b$", "", msg.strip()).strip()
            return result
        elif model_name == "rf-ce-pr_process":
            msg = ""
            if valid_fields.get('Action') == "show":
                if valid_fields.get('Time'): msg = f"show me PRs to approve {valid_fields['Time']}"
            elif valid_fields.get('Action') == "approve":
                if valid_fields.get('PR'): msg = f"please approve the PR number {valid_fields['PR']}"
            elif valid_fields.get('Action') == "disapprove":
                if valid_fields.get('PR'): msg = f"Please disapprove PR number {valid_fields['PR']}"
            return msg
        elif model_name == "rf-ce-room_vehicle_booking":
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

    def configure_sentence_filter(self, filters: SentenceFilters, context: Context,
                                  interaction: Interaction) -> str:
        pass
