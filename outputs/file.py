from .output_manager import AbstractOutput
import argparse
import os


class FileOutput(AbstractOutput):
    tag = "file"
    description = "Saves the report to a file"

    def configure_parser(self, parser):
        parser.add_argument(
            'filename',
            help="The path for the output file")
        return parser

    def dump(self, report, args=None):
        # Ensure the path is correct
        filename = os.path.abspath(parsed_args.filename)
        with open(filename, 'w') as f:
            f.write(report)
