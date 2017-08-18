"""
Application source for the gisrep issues reporter tool
"""

from .cli import Cli
from .config import Config
from .templates.template_manager import TemplateManager, TOOL_TEMPLATE_DIR
from .outputs.output_manager import OutputManager
from github import Github
import getpass
import sys
import os

DEFAULT_CONFIG_PATH = os.path.expanduser("~")
DEFAULT_CONFIG_FILE = ".gisrep_config"
DEFAULT_CONFIG_FILEPATH = os.path.join(DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FILE)

def main():
    """
    Main function, executed upon

    :returns:   None
    :rtype:     None
    """

    # Prepare handlers
    handlers = {
        'init': init,
        'report': report,
        'list': list_component,
    }
    # Parse command line arguments
    cli = Cli(handlers)
    cli.parse(sys.argv[1:])

def init(args):
    """
    Initialises the tool config file

    :param      args:  The command arguments
    :type       args:  argparse.Namespace

    :returns:   None
    :rtype:     None
    """

    # Prompt for username and password
    # TODO: Should this be in Cli?
    username = input("Github username:")
    password = getpass.getpass("Github password:")

    initial_config = {
        'username': username,
        'password': password,
    }

    # Initialise config file
    config = Config(
        DEFAULT_CONFIG_FILEPATH,
        initial_config=initial_config,
        force=args.force)

def report(args):
    """
    Publishes a report using specified query, template and output

    :param      args:  The command arguments
    :type       args:  argparse.Namespace

    :returns:   None
    :rtype:     None
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
    report = builder.generate(
        template_tag,
        issues)

    # Output report
    output.publish(report)

def list_component(args):
    """
    Lists the templates available for publishing

    :param      args:  The command arguments
    :type       args:  argparse.Namespace

    :returns:   None
    :rtype:     None
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
    """
    Entry point for the tool
    """

    main()
