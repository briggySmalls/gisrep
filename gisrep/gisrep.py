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
        'list_templates': list_templates,
        'add_templates': add_templates,
        'remove_templates': remove_templates,
        'list_outputs': list_outputs,
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

    # Read in the existing config
    config = Config()
    # Create the managers based on config/cli args
    # Note: we do this now to catch errors before any API calls
    template_dirs = [TOOL_TEMPLATE_DIR]
    template_dirs.extend(config.template_dirs)
    builder = TemplateManager(template_dirs)
    output_manager = OutputManager()
    output = output_manager.get_output(args.output)

    # Instantiate an API client
    credentials = config.get_credentials()
    api = Github(
        credentials['username'],
        credentials['password'])

    # Request the issues
    issues = api.search_issues(
        args.query)

    # Generate report
    report = builder.generate(
        args.template,
        issues)

    # Output report
    output.publish(report)

def list_templates(args):
    """
    Lists the templates available for publishing
    
    :param      args:  The command arguments
    :type       args:  argparse.Namespace
    
    :returns:   None
    :rtype:     None
    """

    config = Config()
    template_dirs = [TOOL_TEMPLATE_DIR]
    template_dirs.extend(config.template_dirs)
    builder = TemplateManager(template_dirs)
    for template in builder.list():
        print(template)

def add_templates(args):
    """
    Adds a template directory to the config file
    
    :param      args:  The command arguments
    :type       args:  argparse.Namespace
    
    :returns:   None
    :rtype:     None
    """

    config = Config()
    config.add_template_dir(args.directory)

def remove_templates(args):
    """
    Removes a template directory from the config file
    
    :param      args:  The command arguments
    :type       args:  argparse.Namespace
    
    :returns:   None
    :rtype:     None
    """

    config = Config()
    config.remove_template_dir(args.directory)

def list_outputs(args):
    """
    Lists the outputs available for publishing
    
    :param      args:  The command arguments
    :type       args:  argparse.Namespace
    
    :returns:   None
    :rtype:     None
    """

    config = Config()
    output = OutputManager()
    for output in output.list():
        print(output)

if __name__ == '__main__':
    """
    Entry point for the tool
    """

    main()
