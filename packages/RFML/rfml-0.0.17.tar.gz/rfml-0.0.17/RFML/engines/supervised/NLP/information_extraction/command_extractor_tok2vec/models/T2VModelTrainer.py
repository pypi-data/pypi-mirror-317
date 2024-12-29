from RFML.libs.utils import rf


class T2VModelTrainer:
    @staticmethod
    def train(model: str, vector_db_path: str):
        try:
            path = f'{vector_db_path}\\{model}\\corpus'
            rf.cli.spacy_train(
                f'{path}\\config.cfg', f"{vector_db_path}\\{model}", f"{path}\\train.spacy", f"{path}\\dev.spacy"
            )
            return "Model training was successful!"
        except Exception as e:
            print(e)
