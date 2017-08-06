from locate import Locator, Locatable
import outputs
from abc import ABCMeta, abstractmethod
import argparse


class AbstractOutput(Locatable, metaclass=ABCMeta):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description=self.description,
            usage="-o {} [options]".format(self.tag))
        self.parser = self.configure_parser(parser)

    def configure_parser(self, parser):
        return parser

    @abstractmethod
    def dump(self, report, args=None): pass

    @property
    def description(self):
        raise NotImplementedError("description attribute must be defined")


class OutputManager(Locator):
    def __init__(self):
        super().__init__(AbstractOutput)

    def dump(self, args, report):
        # locate the output format using the first argument (tag)
        output_class = self.locate(args[0])
        output = output_class()
        # Generate the report with the report and other arguments
        output.dump(report, args[1:] if len(args) > 0 else None)
