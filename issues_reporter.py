from cli import Cli
from config import Config
from github import Github
from templates.template_manager import TemplateManager
from outputs.output_manager import OutputManager
import getpass
import sys
import os


TOOL_TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'templates')

def init(args):
    # Prompt for username and password
    # TODO: Should this be in Cli?
    username = input("Github username:")
    password = getpass.getpass("Github password:")

    initial_config = {
        'username': username,
        'password': password,
        'template_dirs': [TOOL_TEMPLATE_DIR]
    }

    # Initialise config file
    config = Config(
        initial_config=initial_config,
        force=args.force)

def report(args):
    # Read in the existing config
    config = Config()

    # Instantiate an API client
    credentials = config.get_credentials()
    api = Github(
        credentials['username'],
        credentials['password'])

    # Request the issues
    issues = api.search_issues(
        args.query)

    # Generate report
    builder = TemplateManager(config.template_dirs)
    report = builder.generate(
        args.template,
        issues)

    # Output report
    output = OutputManager()
    output.dump(
        args.output,
        report)

def list_templates(args):
    config = Config()
    builder = TemplateManager(config.template_dirs)
    for template in builder.list():
        print(template)

def list_outputs(args):
    output = OutputManager()
    for output in output.list():
        print(output)

# Get command line arguments
handlers = {
    'init': init,
    'report': report,
    'list_templates': list_templates,
    'list_outputs': list_outputs,
}
cli = Cli(handlers)
cli.parse(sys.argv[1:])
