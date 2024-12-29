from abc import ABC, abstractmethod
from pydoc import Doc
from RFML.core.SentenceFilterConfiguration import SentenceFilterConfiguration


class ISentenceFilter(ABC):
    @abstractmethod
    def configure(self, configuration: SentenceFilterConfiguration):
        pass