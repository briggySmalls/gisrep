from .output_manager import AbstractOutput


class StdOut(AbstractOutput):
    tag = "stdout"

    @classmethod
    def dump(self, report):
        print(report)
