"""
Application source for the gisrep issues reporter tool

Attributes:
    DEFAULT_CONFIG_FILE (str): Default config file name
    DEFAULT_CONFIG_FILEPATH (str): Full file path to default config file
    DEFAULT_CONFIG_DIR (str): Default config file directory
"""

import getpass
import os
import sys

from github import Github

from .cli import Cli
from .config import Config
from .outputs.output_manager import OutputManager
from .templates.template_manager import TOOL_TEMPLATE_DIR, TemplateManager

DEFAULT_CONFIG_DIR = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".gisrep_config"
DEFAULT_CONFIG_FILEPATH = os.path.join(
    os.path.expanduser("~"), DEFAULT_CONFIG_FILE)


def main():
    """Main function for Gisrep tool
    """

    handlers = {
        'init': init,
        'report': report,
        'list': list_component,
    }
    # Parse command line arguments
    cli = Cli(handlers)
    cli.parse(sys.argv[1:])


def init(args):
    """Initialises the tool config file

    Args:
        args (list): Command arguments
    """
    # Prompt for username and password
    username = input("Github username:")
    password = getpass.getpass("Github password:")

    initial_config = {
        'username': username,
        'password': password,
    }

    # Initialise config file
    Config(
        DEFAULT_CONFIG_FILEPATH,
        initial_config=initial_config,
        force=args.force)


def report(args):
    """Publishes a report using specified query, template and output

    Args:
        args (list): Command arguments
    """
    # Create the template manger
    if args.template.endswith('.tplt'):
        # We have been passed a template file path
        template_dir = os.path.dirname(os.path.abspath(args.template))
        template_tag = os.path.splitext(os.path.basename(args.template))[0]
    else:
        # We have been passed a template tag
        template_dir = TOOL_TEMPLATE_DIR
        template_tag = args.template
    builder = TemplateManager(template_dir)

    # Create the output manager, and fetch the output
    output_manager = OutputManager()
    output = output_manager.get_output(args.output)

    if os.path.exists(DEFAULT_CONFIG_FILEPATH):
        # Read in the existing config
        config = Config(DEFAULT_CONFIG_FILEPATH)
        # Instantiate an API client with Github credentials
        credentials = config.get_credentials()
        api = Github(
            credentials['username'],
            credentials['password'])
    else:
        # Instantiate an API client without Github credentials
        api = Github()

    # Request the issues
    issues = api.search_issues(
        args.query)

    # Generate report
    report_obj = builder.generate(
        template_tag,
        issues)

    # Output report
    output.publish(report_obj)


def list_component(args):
    """Lists the templates available for publishing

    Args:
        args (list): Command arguments
    """
    if args.component == 'templates':
        builder = TemplateManager(TOOL_TEMPLATE_DIR)
        for template in builder.list():
            print(template)
    elif args.component == 'outputs':
        output = OutputManager()
        for output in output.list():
            print(output)


if __name__ == '__main__':
    main()
