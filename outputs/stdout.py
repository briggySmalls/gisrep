from .output_manager import AbstractOutput


class StdOutOutput(AbstractOutput):
    tag = "stdout"
    description = "Prints the report to stdout"

    @classmethod
    def dump(self, report, args=None):
        print(report)
