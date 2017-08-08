from .output_manager import AbstractOutput
import pyperclip


class ClipboardOutput(AbstractOutput):
    tag = "clipboard"
    description = "Copies the report to the clipboard"

    @classmethod
    def dump(self, report, args=None):
        pyperclip.copy(report)
