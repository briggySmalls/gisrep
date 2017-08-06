from .output_manager import AbstractOutput
import argparse
import os

FILE_OUTPUT_TAG = "file"

parser = argparse.ArgumentParser(
    description="Saves the report to a file",
    usage="-o {} [options]".format(FILE_OUTPUT_TAG))
parser.add_argument(
    'filename',
    help="The path for the output file")


class FileOutput(AbstractOutput):
    tag = FILE_OUTPUT_TAG

    @classmethod
    def dump(self, report, args=None):
        # Parse the arguments
        parsed_args = parser.parse_args(args)

        # Ensure the path is correct
        filename = os.path.abspath(parsed_args.filename)
        with open(filename, 'w') as f:
            f.write(report)
