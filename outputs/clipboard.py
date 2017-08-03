from .abstract_output import AbstractOutput
import pyperclip


class Clipboard(AbstractOutput):

    @classmethod
    def tag(self):
        return "clipboard"

    @classmethod
    def dump(self, report):
        pyperclip.copy(report)
