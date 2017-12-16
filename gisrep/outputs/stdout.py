"""Output to standard output
"""
from .output_manager import Output


class StdOutOutput(Output):

    """Prints a report to the terminal

    Attributes:
        description (str): Description of the output class
        tag (str): Tag/identifier for the output class
    """

    tag = "stdout"
    description = "Prints the report to stdout"

    @classmethod
    def dump(cls, report, args):
        """Implementation for the dumping of report to std. out

        Args:
            report (str): The report content
            args (list): Further command line options
        """
        print(report)
