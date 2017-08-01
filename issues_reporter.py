from cli import Cli
from config import Config
from api_manager import ApiManager
from template_manager import TemplateManager
from output_manager import OutputManager
import sys


# Parse config file (if it exists)
# TODO: pass cli arg 'config'
config = Config()


def init(args):
    # Initialise config file
    config.init(
        args.username,
        args.password)


def report(args):
    # Request issues
    api = ApiManager(
        config.username,
        config.password)
    issues = api.issues(
        args.repo,
        args.milestone,
        args.labels)

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


# Get command line arguments
cli = Cli(init, report)
cli.parse(sys.argv[1:])
