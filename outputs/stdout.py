from .abstract_output import AbstractOutput


class StdOut(AbstractOutput):

    @classmethod
    def tag(self):
        return "stdout"

    @classmethod
    def dump(self, report):
        print(report)
