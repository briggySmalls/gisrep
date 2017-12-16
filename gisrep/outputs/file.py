"""Output to file
"""
import os

from .output_manager import Output


class FileOutput(Output):

    """Saves a report to a file

    Attributes:
        description (str): Description of the output class
        tag (str): Tag/identifier for the output class
    """

    tag = "file"
    description = "Saves the report to a file"

    @classmethod
    def configure_parser(cls, parser):
        """Adds a filename argument to the command line password

        Args:
            parser (ArgumentParser): Unconfigured parser

        Returns:
            ArgumentParser: Configured parser
        """
        parser.add_argument(
            'filename',
            help="The path for the output file")
        return parser

    @classmethod
    def dump(cls, report, args):
        """Implementation for the dumping of report to file

        Args:
            report (str): The report content
            args (list): Further command line options
        """
        filename = os.path.abspath(args.filename)
        with open(filename, 'w') as file:
            file.write(report)
