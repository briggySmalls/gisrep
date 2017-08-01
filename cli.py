import argparse


class Cli(object):
    def __init__(self, init_handler, report_handler):
        # Build a parser
        parser = argparse.ArgumentParser(
            "Tool for publishing reports of Github issues")
        subparsers = parser.add_subparsers(
            title="commands")

        # Create the parser for the 'init' command
        init_parser = subparsers.add_parser(
            'init',
            help="Initialises the tool to access Github")
        init_parser.add_argument(
            '-f', '--force',
            action='store_true',
            help="Overwrite an existing config file")
        init_parser.add_argument(
            '-l', '--local',
            action='store_true',
            help="Save config file in execution directory")
        init_parser.set_defaults(handler=init_handler)

        # Create the parser for the 'report' command
        report_parser = subparsers.add_parser(
            'report',
            help="Publishes a report from Github issues")
        report_parser.add_argument(
            'template',
            help="Template format to publish issues with")
        report_parser.add_argument(
            '-r', '--repo',
            help="Github repository to query for issues")
        report_parser.add_argument(
            '-m', '--milestone',
            help="Repo milestone to filter issues")
        report_parser.add_argument(
            '-l', '--labels',
            nargs='*',
            help="Labels to filter issues")
        report_parser.add_argument(
            '-o', '--output',
            help="Method to output results")
        report_parser.set_defaults(handler=report_handler)

        # Save the parser
        self.parser = parser

    def parse(self, raw_args):
        args = self.parser.parse_args(raw_args)
        args.handler(args)
