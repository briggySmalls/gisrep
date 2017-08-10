from ..locate import Locator, Locatable
from abc import ABCMeta, abstractmethod
import argparse


class AbstractOutput(Locatable, metaclass=ABCMeta):
    def __init__(self, args):
        parser = argparse.ArgumentParser(
            description=self.description,
            usage="-o {} [options]".format(self.tag))
        self.parser = self.configure_parser(parser)
        self.parsed_args = self.parser.parse_args(args)

    def configure_parser(self, parser):
        return parser

    def publish(self, report):
        # Dump the report
        self.dump(report, self.parsed_args)

    @abstractmethod
    def dump(report, args=None): pass

    @property
    def description(self):
        raise NotImplementedError("description attribute must be defined")


class OutputManager(Locator):
    def __init__(self):
        super().__init__(AbstractOutput)

    def get_output(self, args):
        return self.locate(args[0])(args[1:] if len(args) > 1 else [])
