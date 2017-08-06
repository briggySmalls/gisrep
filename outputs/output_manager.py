from locate import Locator, Locatable
import outputs
from abc import ABCMeta, abstractmethod


class AbstractOutput(Locatable, metaclass=ABCMeta):
    @abstractmethod
    def dump(self, report, args=None): pass


class OutputManager(Locator):
    def __init__(self):
        super().__init__(AbstractOutput)

    def dump(self, args, report):
        # locate the output format using the first argument (tag)
        output_class = self.locate(args[0])
        output = output_class()
        # Generate the report with the report and other arguments
        output.dump(report, args[1:] if len(args) > 0 else None)
