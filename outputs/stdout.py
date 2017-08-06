from .output_manager import AbstractOutput


class StdOutOutput(AbstractOutput):
    tag = "stdout"

    @classmethod
    def dump(self, report, args=None):
        print(report)
