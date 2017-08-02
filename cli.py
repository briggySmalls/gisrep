import argparse


class Cli(object):
    def __init__(self, init_handler, report_handler):
        # Build a parser
        parser = argparse.ArgumentParser(
            "Tool for publishing reports of Github issues")
        subparsers = parser.add_subparsers(
            title="commands")
        self._add_init_parser(subparsers, init_handler)
        self._add_report_parser(subparsers, report_handler)
        # Save the parser
        self.parser = parser

    def _add_init_parser(self, subparsers, init_handler):
        # Create the parser for the 'init' command
        init_parser = subparsers.add_parser(
            'init',
            help="Initialises the tool to access Github")
        init_parser.add_argument(
            '-f', '--force',
            action='store_true',
            help="Overwrite an existing config file")
        init_parser.set_defaults(handler=init_handler)

    def _add_report_parser(self, subparsers, report_handler):
        # Create the parser for the 'report' command
        report_parser = subparsers.add_parser(
            'report',
            help="Publishes a report from Github issues")
        report_parser.add_argument(
            'template',
            help="Template format to publish issues with")
        report_parser.add_argument(
            '-q', '--query',
            help="Github issues search query (see https://help.github.com/articles/searching-issues-and-pull-requests/)")
        report_parser.add_argument(
            '-o', '--output',
            default="stdout",
            help="Method to output results")
        report_parser.set_defaults(handler=report_handler)

    def parse(self, raw_args):
        args = self.parser.parse_args(raw_args)
        args.handler(args)
