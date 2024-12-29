import uuid
import re
import language_tool_python

from RFML.api.ServiceApi import ServiceApi
from RFML.core.CacheMixin import CacheMixin
from RFML.core.Cognitive import Cognitive
from RFML.core.Conversation import Context
from RFML.core.Interaction import Interaction, TaskType
from RFML.core.Results import PredictResult, TrainResult, GenerateResult, ResultType
from RFML.core.Router import Router
from RFML.core.SentenceFilterConfiguration import SentenceFilterConfiguration
from RFML.core.SentenceFilters import SentenceFilters
from RFML.interface.ICognitive import ICognitive
from RFML.interface.IOptions import IOptions
from RFML.libs.core.SentenceValidator import SentenceValidator
from RFML.prompt.Prompt import Prompt
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery


class RFML:
    cognitive = Cognitive("", "", None, None, False)  # cognitive
    cognitive_handler = ICognitive  # cognitive configure
    _filter = SentenceFilters()

    def __init__(self, cognitive: ICognitive, prompt: Prompt = None, options: IOptions = None):
        print('RFML is being initialized...')
        self.cognitive_handler = cognitive
        print('Loading language library...')
        self.lang_tool = language_tool_python.LanguageTool('en-US', config={'cacheSize': 1000,
                                                                            'pipelineCaching': True,
                                                                            'maxSpellingSuggestions': 0})  # Initialize the LanguageTool instance
        self.lang_tool.check("Hi")
        print('Engine is now ready to use...')

        # no need here
        if self.cognitive_handler is not None:
            self.cognitive_handler.configure(self.cognitive)

        # invoke API or CLI with a callback
        if prompt: prompt.invoke_prompt(self.core_process_callback)

    def switch_cognitive(self, model_name: str):
        # if not self.cognitive.modules: return
        if model_name:
            if self.cognitive.modules:
                cognitive = Cognitive("", "", None, None, False)
                items = self.cognitive.modules.modules
                _engine = [item for item in items if item.model_name == model_name]

                if _engine:
                    _engine[0].engine.configure(cognitive)
                    self.cognitive = cognitive
                    return cognitive
            else:
                self.cognitive_handler.configure(self.cognitive)
                return self.cognitive

    def __reload(self, interaction: Interaction):
        old_cognitive = self.cognitive
        if self.cognitive.model != interaction.model:
            _cognitive = self.switch_cognitive(interaction.model)
            if _cognitive:
                self.cognitive = _cognitive
            else:
                return "Sorry, model was not found to reload!"

        self.cognitive.handlers.predictor.reload_model(self.cognitive.model, self.cognitive.corpus)
        self.cognitive = old_cognitive
        return "Model is reload!"

    # main process (callback from API/CLI)
    def core_process_callback(self, interaction: Interaction):
        # load default model
        if self.cognitive.modules:
            if interaction.session_id:
                context: Context = self.cognitive.corpus.context.read({"session_id": interaction.session_id})
                if context:
                    if self.cognitive.model != context.model:
                        if self.cognitive.modules:
                            _cognitive = self.switch_cognitive(context.model)
                            if _cognitive: self.cognitive = _cognitive
                else:
                    self.cognitive_handler.configure(self.cognitive)
            else:
                self.cognitive_handler.configure(self.cognitive)

        predict_result = PredictResult()

        if self.cognitive_handler is not None:
            match interaction.task:  # from Prompt Interaction (API/CLI)
                case TaskType.Reload:
                    return self.__reload(interaction)
                case TaskType.Train:
                    train_msg = self.__train(interaction)
                    if train_msg.success:
                        reload_msg = self.__reload(interaction)
                        return f"{train_msg.message}. {reload_msg}."
                    else:
                        return f"{train_msg.message}."
                case TaskType.Generate:
                    msg = self.__generate(interaction)
                    return f"{msg.message}"
                case TaskType.Predict | _:  # predict or default incoming INPUT

                    if interaction.session_id == "":
                        predict_result = self.__predict(interaction)  # pass session_id to return from PredictResult
                    else:  # has a session_id
                        CacheMixin.log_conversation(interaction, self.cognitive)  # log conversation

                        # Journey Start Here
                        pc: PromptCash = self.cognitive.corpus.prompt_cash.read({"session_id": interaction.session_id})
                        if pc:  # check PC
                            prompt_queries = []
                            # configure prompt instruction and prepare validator JSON
                            # equivalent to self.__load_prompt_queries(prompt_queries)
                            if self.cognitive.handlers.validator:
                                self.cognitive.handlers.validator.configure_prompt_queries(self.cognitive.model,
                                                                                           prompt_queries)
                                prompt_result = CacheMixin.process_prompt(
                                    pc=pc,
                                    interaction=interaction, cognitive=self.cognitive,
                                    predict_result=predict_result, prompt_queries=prompt_queries,
                                )
                                if prompt_result:  # prompt_result not empty, keep asking prompt
                                    predict_result = prompt_result
                                else:  # prompt_result is None, so no more prompt
                                    # prompt process completed. check value for decision
                                    passed, canceled = False, False
                                    _valid_fields: any
                                    valid_fields = {}
                                    for key, value in pc.validator_cash.items():
                                        if value == "__canceled__":
                                            predict_result.message = "The request has been canceled!"
                                            self.cognitive.corpus.prompt_cash.update(interaction.session_id, {})
                                            canceled = True
                                            break
                                        else:
                                            # rander partial format
                                            for cash_key, cash_value in pc.validator_cash.items():
                                                if cash_value != "__passed__":
                                                    valid_fields[cash_key] = cash_value
                                                else:
                                                    passed = True

                                    if not canceled:
                                        _valid_fields = valid_fields if passed else pc.validator_cash

                                        correct = self.cognitive.handlers.validator.format_prompt_queries(
                                            self.cognitive.model, pc, _valid_fields, interaction.input
                                        )
                                        if correct: interaction.input = correct
                                        predict_result = self.__predict(interaction)
                            else:
                                predict_result = self.__predict(interaction)
                        else:  # predict
                            predict_result = self.__predict(interaction)

                    if self.cognitive:
                        # if predict_result.result_type == ResultType.do_not_understand and self.cognitive.gateway == False:
                        if not self.cognitive.gateway and predict_result.result_type == ResultType.do_not_understand:
                            self.cognitive_handler.configure(self.cognitive)
                            predict_result = self.__predict(interaction)
                    else:
                        self.cognitive = Cognitive("", "", None, None, False)  # cognitive
                        self.cognitive_handler.configure(self.cognitive)
                        return {
                            "msg": predict_result.message,
                            "model": '',
                            "id": ''
                        }  # .message  # predict or default outgoing OUTPUT

                    predict_result.session_id = interaction.session_id or str(uuid.uuid4())
                    predict_result.model = self.cognitive.model
                    CacheMixin.log_context(self.cognitive, interaction, predict_result)  # log context

                    return {
                        "msg": predict_result.message,
                        "model": self.cognitive.model,
                        "id": predict_result.session_id
                    }  # .message  # predict or default outgoing OUTPUT

    # organic
    def predict(self, text: str) -> PredictResult:
        interaction = Interaction("", self.cognitive.model, TaskType.Predict, text)
        self.core_process_callback(interaction)
        return self.__predict(interaction)

    # organic
    def train(self, model: str) -> TrainResult:
        interaction: Interaction = Interaction("", model, TaskType.Train, "")
        self.core_process_callback(interaction)
        return self.__train(interaction)

    # organic
    def generate(self, model: str) -> GenerateResult:
        interaction: Interaction = Interaction("", model, TaskType.Train, "")
        return self.__generate(interaction)

    def __load_prompt_queries(self, prompt_queries=None):
        if prompt_queries is None: prompt_queries = []
        if self.cognitive.handlers.validator:
            self.cognitive.handlers.validator.configure_prompt_queries(self.cognitive.model, prompt_queries)

    def is_correct_sentence(self, interaction) -> (bool, str):
        # validate incomplete input (sentence)
        correct = True
        _config = SentenceFilterConfiguration()
        if self.cognitive.handlers.validator:
            context: Context = Context(self.cognitive.model, "")
            self.cognitive.handlers.validator.configure_sentence_filter(self._filter, context, interaction)

        doc = _config.nlp(interaction.input)
        if len(doc) < 3:
            lowered = [item.lower().strip() for item in self._filter.one_word_patterns]
            if lowered and interaction.input.strip().lower() not in lowered: correct = False
        else:
            # block_inputs = ' '.join(interaction.input.split()).replace("?", "")
            # if block_inputs in self._filter.block_sentences_patterns:
            #     correct = False
            doc = _config.nlp(interaction.input)
            _config.matcher.add("INVALID_SENTENCES", self._filter.match_invalid_patterns)
            if _config.matcher(doc):
                correct = False
            else:
                sv = SentenceValidator()
                correct, root_lemma = sv.validate_sentence(self.lang_tool, interaction.input)  # improve here
                # correct, root_lemma = sv.validate_sentence(_config.nlp, interaction.input)  # improve here
                # if correct: correct = sv.is_valid_pattern(self._filter, interaction, root_lemma)

        return correct, _config.default_message
        # end validate incomplete input (sentence)

    # lower predict function is called from API and Lib
    def __predict(self, interaction: Interaction) -> PredictResult:
        correct, message = self.is_correct_sentence(interaction)
        if not correct:
            return PredictResult(
                session_id=interaction.session_id or str(uuid.uuid4()),
                result_type=ResultType.invalid_input, message=message,
                input_text=interaction.input
            )
            # return {"msg": pr.message, "id": pr.session_id}

        prompt_queries = []

        # configure prompt instruction and prepare validator JSON
        # if self.cognitive.handlers.validator:
        #     self.cognitive.handlers.validator.configure_prompt_queries(self.cognitive.model, prompt_queries)

        if interaction.session_id == "":  # first predict call as no session_id
            # process input before predict
            before_predict_text = \
                self.cognitive.handlers.predictor.before_predict(self.cognitive.model, interaction.input)
            before_predict_text = before_predict_text or interaction.input

            self.__load_prompt_queries(prompt_queries)
            predict_result = \
                self.cognitive.handlers.predictor.predict(self.cognitive.model, before_predict_text,
                                                          self.cognitive.corpus)

            # do_not_understand => in case of same cognitive but different model
            if predict_result.result_type == ResultType.do_not_understand:
                if not self.cognitive.modules:
                    self.cognitive_handler.configure(self.cognitive)
                    self.__load_prompt_queries(prompt_queries)
                    predict_result = \
                        self.cognitive.handlers.predictor.predict(self.cognitive.model, before_predict_text,
                                                                  self.cognitive.corpus)

            predict_result.input_text = interaction.input
            predict_result.model = self.cognitive.model

            # routing
            if predict_result.route:
                if predict_result.route == "cb" or predict_result.route == "callback":
                    predict_result = self.cognitive.handlers.predictor.on_model_callback(predict_result)
                else:
                    self.cognitive = self.switch_cognitive(predict_result.route)
                    predict_result = Router.redirect(self.cognitive, prompt_queries, before_predict_text)

            if predict_result.result_type == ResultType.do_not_understand: return predict_result

            if self.cognitive.handlers.validator:  # validate model
                mismatch = PromptQuery.validate(
                    interaction.session_id, predict_result, prompt_queries, self.cognitive.corpus
                )
                if not mismatch.valid:  # not a valis predict
                    return PredictResult(
                        session_id=interaction.session_id,
                        label=predict_result.label,
                        probability=0.0,
                        message=mismatch.message,  # "what is the room name",
                        route=""
                    )
                else:
                    self.cognitive.corpus.prompt_cash.update(interaction.session_id, {})  # empty

        else:  # else session_id exists so loop through prompt query
            # process input before predict
            before_predict_text = \
                self.cognitive.handlers.predictor.before_predict(self.cognitive.model, interaction.input)
            before_predict_text = before_predict_text or interaction.input

            self.__load_prompt_queries(prompt_queries)
            predict_result = \
                self.cognitive.handlers.predictor.predict(self.cognitive.model, before_predict_text,
                                                          self.cognitive.corpus)

            # do_not_understand => in case of same cognitive but different model .. working how?
            if predict_result.result_type == ResultType.do_not_understand:
                if not self.cognitive.modules:
                    self.cognitive_handler.configure(self.cognitive)
                    self.__load_prompt_queries(prompt_queries)
                    predict_result = \
                        self.cognitive.handlers.predictor.predict(self.cognitive.model, before_predict_text,
                                                                  self.cognitive.corpus)

            predict_result.input_text = interaction.input
            predict_result.model = self.cognitive.model

            # routing
            if predict_result.route:
                if predict_result.route == "cb" or predict_result.route == "callback":
                    predict_result = self.cognitive.handlers.predictor.on_model_callback(predict_result)
                else:
                    self.cognitive = self.switch_cognitive(predict_result.route)
                    predict_result = Router.redirect(self.cognitive, prompt_queries, before_predict_text)

            if predict_result.result_type == ResultType.do_not_understand: return predict_result  # ==>

            if self.cognitive.handlers.validator:  # validate model
                mismatch = PromptQuery.validate(
                    interaction.session_id, predict_result, prompt_queries, self.cognitive.corpus
                )
                if not mismatch.valid:  # not a valis predict
                    return PredictResult(  # ==>
                        session_id=interaction.session_id,
                        label=predict_result.label,
                        probability=0.0,
                        message=mismatch.message,  # "what is the room name",
                        route=""
                    )
                else:
                    self.cognitive.corpus.prompt_cash.update(interaction.session_id, {})  # empty

        api = ServiceApi()
        # process input after predict
        return self.cognitive.handlers.predictor.after_predict(self.cognitive.model, predict_result, api)

    # lower train function
    def __train(self, interaction: Interaction) -> TrainResult:
        old_cognitive = self.cognitive
        if self.cognitive.model != interaction.model:
            _cognitive = self.switch_cognitive(interaction.model)
            if _cognitive:
                self.cognitive = _cognitive
            else:
                return TrainResult(
                    message="Sorry, model was not found for training!"
                )

        dataset = self.cognitive.corpus.cognitive.read({"model": interaction.model})
        dataset_class = self.cognitive.corpus.training_corpus.from_json(dataset)

        # for item in self.cognitive.modules.modules:
        #     item.engine.meta.conitive_skill

        _corpus = self.cognitive.corpus
        self.cognitive.handlers.trainer.before_train(self.cognitive.model, dataset_class, _corpus)
        training_result = self.cognitive.handlers.trainer.train(self.cognitive.model, dataset_class, _corpus)
        self.cognitive.handlers.trainer.after_train(self.cognitive.model, dataset_class, _corpus)

        self.cognitive = old_cognitive
        return training_result

    # lower generate function
    def __generate(self, interaction: Interaction) -> GenerateResult:
        old_cognitive = self.cognitive
        if self.cognitive.model != interaction.model:
            _cognitive = self.switch_cognitive(interaction.model)
            if _cognitive:
                self.cognitive = _cognitive
            else:
                return GenerateResult(
                    message="Sorry, model was not found for data_gen generation!"
                )

        command = self.command_generator(interaction)

        dataset = self.cognitive.corpus.cognitive.read({"model": interaction.model})
        dataset_class = self.cognitive.corpus.training_corpus.from_json(dataset)

        _corpus = self.cognitive.corpus
        self.cognitive.handlers.generator.before_generate(self.cognitive.model, dataset_class, _corpus)
        generate_result = self.cognitive.handlers.generator.generate(self.cognitive.model, dataset_class, _corpus,
                                                                     command)
        self.cognitive.handlers.generator.after_generate(self.cognitive.model, dataset_class, _corpus)

        self.cognitive = old_cognitive
        return generate_result

    def command_generator(self, interaction: Interaction):
        if isinstance(interaction.input, dict):
            return interaction.input
        else:
            cmd = interaction.input.strip().replace('rf gen', '')
            info = cmd.split()
            if info[1] == "split":
                # rf gen rf-ce-on_desk_booking split 0.8
                return {
                    "command": info[1],  # split
                    "index": info[2] if len(info) > 2 else 0.8  # split index
                }
            elif info[1] == "make":
                # rf gen rf-ce-on_desk_booking make spacy
                return {
                    "command": info[1],  # make
                    "make_type": info[2] if len(info) > 2 else 'spacy'  # make_type
                }
            elif info[1] == "split_make":
                # rf gen rf-ce-on_desk_booking split_make
                return {
                    "command": info[1],  # split_make
                    "make_type_index": [info[2] if len(info) > 2 else 0.8, 'spacy']  # make_type_index
                }
            elif info[1] == "entity":
                # rf gen rf-ce-on_desk_booking entity
                return {
                    "command": info[1]  # split_make
                }
            elif info[1] == "all":
                # rf gen rf-ce-on_desk_booking entity
                return {
                    "command": info[1],  # split_make
                    "make_type_index": [info[2] if len(info) > 2 else 0.8, 'spacy']
                }
