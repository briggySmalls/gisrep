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

# Create a parser for the 'templates' command
templates_parser = subparsers.add_parser(
    'templates',
    help="Manage report templates")
templates_subparsers = templates_parser.add_subparsers(
    title="commands",
    dest="command")
templates_subparsers.required = True

# Create a parser for the 'templates list' command
list_templates_parser = templates_subparsers.add_parser(
    'list',
    help="List the available templates")

# Create a parser for the 'templates add' command
add_templates_parser = templates_subparsers.add_parser(
    'add',
    help="Add templates to the tool")
add_templates_parser.add_argument(
     'directory',
     help="Adds directory to the template path")

# Create a parser for the 'templates remove' command
remove_templates_parser = templates_subparsers.add_parser(
     'remove',
     help="Remove templates from the tool")
remove_templates_parser.add_argument(
     'directory',
     help="Removes directory from the template path") 

# Create a parser for the 'outputs' command
outputs_parser = subparsers.add_parser(
    'outputs',
    help="Manage output methods")
outputs_subparsers = outputs_parser.add_subparsers(
    title="commands",
    dest="command")
outputs_subparsers.required = True

# Create a parser for the 'outputs list' command
list_outputs_parser = outputs_subparsers.add_parser(
    'list',
    help="List the available output methods")

class Cli(object):
    def __init__(self, handlers):
        self._set_handler(init_parser, handlers['init'])
        self._set_handler(report_parser, handlers['report'])
        self._set_handler(list_templates_parser, handlers['list_templates'])
        self._set_handler(add_templates_parser, handlers['add_templates'])
        self._set_handler(remove_templates_parser, handlers['remove_templates'])
        self._set_handler(list_outputs_parser, handlers['list_outputs'])

    def parse(self, raw_args):
        args = root_parser.parse_args(raw_args)
        args.handler(args)

    def _set_handler(self, parser, handler):
        parser.set_defaults(handler=handler)
