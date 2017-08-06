from .output_manager import AbstractOutput
import pyperclip


class ClipboardOutput(AbstractOutput):
    tag = "clipboard"

    @classmethod
    def dump(self, report, args=None):
        pyperclip.copy(report)
