"""
Module that defines behaviour of command line interface
"""

import argparse

# Build a parser
root_parser = argparse.ArgumentParser(
    description="Tool for publishing reports of Github issues")
subparsers = root_parser.add_subparsers(
    title="commands",
    dest="command")
subparsers.required = True

# Create a parser for the 'init' command
init_parser = subparsers.add_parser(
    'init',
    help="Initialises the tool to access Github")
init_parser.add_argument(
    '-f', '--force',
    action='store_true',
    help="Overwrite an existing config file")

# Create a parser for the 'report' command
report_parser = subparsers.add_parser(
    'report',
    help="Publishes a report from Github issues")
report_parser.add_argument(
    'template',
    help="Template format to publish issues with")
report_parser.add_argument(
    'query',
    help="Github issues search query (see https://help.github.com/articles/searching-issues-and-pull-requests/)")
report_parser.add_argument(
    '-o', '--output',
    default=["stdout"],
    nargs='+',
    help="Method to output results")

# Create a parser for the 'list' subcommand
list_parser = subparsers.add_parser(
    'list',
    help="List built-in components")
list_parser.add_argument(
    'component',
    choices=['templates', 'outputs'],
    help="Component to list built-ins for")

class Cli(object):
    def __init__(self, handlers):
        """
        Class for cli.

        :returns:   CLI object that calls handlers defined in constructor
        :rtype:     Cli
        """

        self.set_handler(init_parser, handlers['init'])
        self.set_handler(report_parser, handlers['report'])
        self.set_handler(list_parser, handlers['list'])

    def parse(self, raw_args):
        """
        Parses the arguments

        :param      raw_args:  The raw arguments
        :type       raw_args:  list

        :returns:   None
        :rtype:     None
        """

        args = root_parser.parse_args(raw_args)
        args.handler(args)

    def set_handler(self, parser, handler):
        """
        Sets a handler for the parser

        :param      parser:   The parser
        :param      handler:  The handler function
        :type       parser:   argparse.ArgumentParser
        :type       handler:  function

        :returns:   None
        :rtype:     None
        """

        parser.set_defaults(handler=handler)
