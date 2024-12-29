from RFML.core.Results import PredictResult, ResultType


class Router:
    @staticmethod
    def redirect(cognitive, prompt_queries, before_predict_text) -> PredictResult:
        prompt_queries.clear()

        if cognitive:
            if cognitive.handlers.validator:
                cognitive.handlers.validator.configure_prompt_queries(cognitive.model, prompt_queries)
            predict_result = cognitive.handlers.predictor.predict(cognitive.model, before_predict_text,
                                                                  cognitive.corpus)
            return predict_result
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand,
                message="Sorry, I don’t have the information you need right now. We might include this in the future!"
            )
