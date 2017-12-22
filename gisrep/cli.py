"""
Module that defines behaviour of command line interface
"""

import argparse


class Cli(object):  # pylint: disable=too-few-public-methods

    """Class for parsing command line arguments

    Attributes:
        root_parser (ArgumentParser): Gisrep parser

    """

    def __init__(self, handlers):
        # Build a parser
        self.root_parser = argparse.ArgumentParser(
            description="Tool for publishing reports of Github issues")
        subparsers = self.root_parser.add_subparsers(
            title="commands",
            dest="command")
        subparsers.required = True

        self._add_init_parser(subparsers, handlers['init'])
        self._add_report_parser(subparsers, handlers['report'])
        self._add_list_parser(subparsers, handlers['list'])

    @classmethod
    def _add_init_parser(cls, subparsers, handler):
        """Creates a subparser for the init command

        Args:
            subparsers (argparse._SubParsersAction): Subparsers
            handler (function): Handler for init command
        """

        init_parser = subparsers.add_parser(
            'init',
            help="Initialises the tool to access Github")
        init_parser.add_argument(
            '-f', '--force',
            action='store_true',
            help="Overwrite an existing config file")
        init_parser.set_defaults(handler=handler)

    @classmethod
    def _add_report_parser(cls, subparsers, handler):
        """Creates a subparser for the report command

        Args:
            subparsers (argparse._SubParsersAction): Subparsers
            handler (function): Handler for report command
        """

        report_parser = subparsers.add_parser(
            'report',
            help="Publishes a report from Github issues")
        report_parser.add_argument(
            'query',
            help=(
                "Github issues search query (see "
                "help.github.com/articles/"
                "searching-issues-and-pull-requests/)"))
        group = report_parser.add_mutually_exclusive_group()
        group.add_argument(
            '-t', '--template',
            default='simple_report.md',
            help="Tag of internal template to format issues with")
        group.add_argument(
            '-u', '--user-template',
            help="Path to user template to format issues with")
        report_parser.set_defaults(handler=handler)

    @classmethod
    def _add_list_parser(cls, subparsers, handler):
        """Creates a subparser for the list command

        Args:
            subparsers (argparse._SubParsersAction): Subparsers
            handler (function): Handler for list subcommand
        """

        list_parser = subparsers.add_parser(
            'list',
            help="List built-in templates")
        list_parser.set_defaults(handler=handler)

    def parse(self, raw_args):
        """Parses command line arguments

        Args:
            raw_args (list): Command line arguments
        """

        args = self.root_parser.parse_args(raw_args)
        args.handler(args)
