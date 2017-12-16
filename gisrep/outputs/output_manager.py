"""Manager logic for passing report to output
"""
import argparse

from ..locate import Locatable, Locator


class Output(Locatable):

    """Abstract class for producing an output from a report

    Attributes:
        parsed_args (argparse.Namespace): Parsed arguments object

    """

    def __init__(self, args):
        parser = argparse.ArgumentParser(
            description=self.description,
            usage="-o {}".format(self.tag))
        parser = self.configure_parser(parser)
        self.parsed_args = parser.parse_args(args)

    @property
    def description(self):
        """Returns the tag for the Locatable class

        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError(
            "description attribute must be defined on Output class")

    @classmethod
    def configure_parser(cls, parser):
        """Configures an output parser for the command line

        Args:
            parser (ArgumentParser): Base parser for Ouput

        Returns:
            ArgumentParser: Configured parser
        """
        return parser

    @classmethod
    def dump(cls, report, args):
        """Dumps a report to its output

        Args:
            report (str): The report content
            args (list): Output-specific command line arguments

        Raises:
            NotImplementedError: The dump function must be defined on Output
                                 classes
        """
        raise NotImplementedError(
            "dump method must be defined on Output class")

    def publish(self, report):
        """Publishes the report

        Args:
            report (str): The report to publish
        """

        self.dump(report, self.parsed_args)


class OutputManager(Locator):

    """Class for locating output clases
    """

    def __init__(self):
        super().__init__(Output)

    def get_output(self, args):
        """

        Args:
            args (list): Command line arguments specifying output

        Returns:
            Output: Output object
        """
        return self.locate(args[0])(args[1:] if len(args) > 1 else [])
