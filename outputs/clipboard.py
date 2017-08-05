from .output_manager import AbstractOutput
import pyperclip


class Clipboard(AbstractOutput):
    tag = "clipboard"

    @classmethod
    def dump(self, report):
        pyperclip.copy(report)
