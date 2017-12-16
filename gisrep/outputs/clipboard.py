"""Output to clipboard
"""
import pyperclip

from .output_manager import Output


class ClipboardOutput(Output):

    """Copies the report to the clipboard

    Attributes:
        description (str): Description of the output class
        tag (str): Tag/identifier for the output class
    """

    tag = "clipboard"
    description = "Copies the report to the clipboard"

    @classmethod
    def dump(cls, report, args):
        """Implementation for the dumping of report to clipboard

        Args:
            report (str): The report content
            args (None, optional): Further command line options
        """
        pyperclip.copy(report)
