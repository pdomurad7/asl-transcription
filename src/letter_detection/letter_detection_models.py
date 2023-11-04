import logging
from abc import abstractmethod

import numpy as np
from tensorflow.keras.models import load_model

from .analysis_model_utils.hand import Hand
from .analysis_model_utils.letters import letters
from .nn_model_utils.letters import Letters


class LetterDetectionModel:
    def __init__(self, config: dict):
        self.__config = config

    @abstractmethod
    def predict(self, xs, ys, zs) -> str | None:
        pass


class AnalysisModel(LetterDetectionModel):
    def predict(self, xs, ys, zs) -> str | None:
        hand = Hand(xs, ys, zs)
        matched_letters = [
            letter.__name__ for letter in letters if letter(hand).check_rules()
        ]
        if len(matched_letters) != 1:
            return None
        return matched_letters[0]


class NNModel(LetterDetectionModel):
    def __init__(self, config: dict):
        super().__init__(config)
        self.__model_path = config["model_path"]
        self.__confident_threshold = config["confident_threshold"]
        self.__model = None
        self.__initialize_model()

    def __initialize_model(self):
        self.__model = load_model(self.__model_path)

    def predict(self, xs, ys, zs) -> str | None:
        data_to_predict = np.array([xs + ys + zs])
        prediction = self.__model.predict(data_to_predict, verbose=0    )[0]
        if np.max(prediction) < self.__confident_threshold:
            return None
        return Letters(np.argmax(prediction)).name


class DecisionTreeModel(LetterDetectionModel):
    def __init__(self, config: dict):
        super().__init__(config)
        self.__model_path = config["model_path"]
        self.__model = None
        self.__initialize_model()

    def __initialize_model(self):
        pass

    def predict(self, xs, ys, zs) -> str | None:
        pass


letter_detection_models = {
    f"{model.__name__}": model for model in LetterDetectionModel.__subclasses__()
}


class LetterDetectionModelFactory:
    @staticmethod
    def create(config: dict) -> LetterDetectionModel:
        model_type = config["model_type"]
        model_config = config.get("model_config", {})
        if model_type in letter_detection_models:
            logging.getLogger("LetterDetectionModelFactory").info(f"Creating {model_type} with config {model_config}")
            return letter_detection_models[model_type](model_config)
        else:
            raise ValueError(
                f"Unknown model type: {model_type}, available models: {letter_detection_models.keys()}"
            )
