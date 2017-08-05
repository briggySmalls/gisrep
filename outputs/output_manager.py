from locate import Locator, Locatable
import outputs
from abc import ABCMeta, abstractmethod


class AbstractOutput(Locatable, metaclass=ABCMeta):
    @abstractmethod
    def dump(self, report): pass


class OutputManager(Locator):
    def __init__(self):
        super().__init__(AbstractOutput)

    def dump(self, tag, report):
        output_class = self.locate(tag)
        output = output_class()
        output.dump(report)
