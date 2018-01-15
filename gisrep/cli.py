"""
Module that defines behaviour of command line interface
"""

import argparse
import os

from .errors import GisrepError


class Cli(object):  # pylint: disable=too-few-public-methods

    """Class for parsing command line arguments

    Attributes:
        root_parser (ArgumentParser): Gisrep parser

    """

    def __init__(self, handlers):
        # Build a parser
        self.root_parser = argparse.ArgumentParser(
            description="Tool for publishing Github issues.")
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
            description=(
                "Creates a '.gisreprc' configuration file to store Github "
                "username and adds the password to the system password "
                "manager."),
            help="Initialise gisrep to use Github credentials")
        init_parser.add_argument(
            '-f', '--force',
            action='store_true',
            help="Overwrite an existing config file")
        init_parser.add_argument(
            '-l', '--local',
            help="Path to a directory in which to save the file")
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
            description=(
                "Publishes a report of nicely formatted Github issues "
                "specified by a Github issues search query "
                "(see help.github.com/articles/"
                "searching-issues-and-pull-requests/)"),
            help="Publish Github issues")

        # Query
        report_parser.add_argument(
            'query',
            help=("Issues search query"))

        # Add mutually exclusive group template/user-template
        template_group = report_parser.add_mutually_exclusive_group()
        template_group.add_argument(
            '-i', '--internal',
            default='simple_report.md',
            help="Tag of internal template to format issues with")
        template_group.add_argument(
            '-e', '--external',
            help="Path to external template to format issues with")
        report_parser.set_defaults(handler=handler)

        # Allow config to be passed to the command line
        report_parser.add_argument(
            '-c', '--config',
            help="Path to gisrep config file")

        # Or have credentials passed in directly
        report_parser.add_argument(
            '-p', '--password',
            help="Github password")
        report_parser.add_argument(
            '-u', '--username',
            help="Github usename")

    @classmethod
    def _add_list_parser(cls, subparsers, handler):
        """Creates a subparser for the list command

        Args:
            subparsers (argparse._SubParsersAction): Subparsers
            handler (function): Handler for list subcommand
        """

        list_parser = subparsers.add_parser(
            'list',
            description=(
                "Lists internal templates shipped with gisrep that may be "
                "used with the 'report' command to format the results."),
            help="List internal templates")
        list_parser.set_defaults(handler=handler)

    def parse(self, raw_args):
        """Parses command line arguments

        Args:
            raw_args (list): Command line arguments
        """

        args = self.root_parser.parse_args(raw_args)

        if args.command == 'report':
            # Verify argument combinations
            if args.username:
                assert args.password
            elif args.password:
                assert args.username
            if args.config and args.username:
                raise GisrepError(
                    "Config file and username/password are mutually exclusive")

            # Confirm files exist
            if args.config and not os.path.exists(args.config):
                raise GisrepError(
                    "Cannot find config file: {}".format(args.config))
            if args.external and not os.path.exists(args.external):
                raise GisrepError(
                    "Cannot find external template: {}".format(args.external))

        args.handler(args)


def get_parser():
    """Gets a CLI parser with no handlers

    Returns:
        TYPE: A Cli object
    """
    return Cli({
        'init': None,
        'report': None,
        'list': None,
    }).root_parser
