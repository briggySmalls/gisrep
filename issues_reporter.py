from cli import Cli
from config import Config
from github import Github
from template_manager import TemplateManager
from output_manager import OutputManager
import getpass
import sys


def init(args):
    # Prompt for username and password
    username = input("Github username:")
    password = getpass.getpass("Github password:")

    credentials = {
        'username': username,
        'password': password,
    }

    # Initialise config file
    config = Config(
        initial_config=credentials,
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
    builder = TemplateManager()
    report = builder.generate(
        args.template,
        issues)

    # Output report
    output = OutputManager()
    output.dump(
        args.output,
        report)

def template(args):
    builder = TemplateManager()
    for template in builder.list():
        print(template)

def outputs(args):
    output = OutputManager()
    for output in output.list():
        print(output)

# Get command line arguments
handlers = {
    'init': init,
    'report': report,
    'templates': template,
    'outputs': outputs,
}
cli = Cli(handlers)
cli.parse(sys.argv[1:])
