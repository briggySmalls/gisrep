from gisrep.cli import Cli

import pytest


def default_handler(args):
    """Default handler for CLI callbacks

    Args:
        args (argparse.Namespace): Command line arguments
    """
    assert False, ("Default handler called with args: {0}".format(args))


@pytest.fixture
def cli_and_handlers():
    # Reset handlers to default
    handlers = {}
    handlers['init'] = default_handler
    handlers['report'] = default_handler
    handlers['list'] = default_handler

    # Instantiate new Cli object
    return Cli(
        {
            'init': lambda args: handlers['init'](args),
            'report': lambda args: handlers['report'](args),
            'list': lambda args: handlers['list'](args),
        }), handlers


def test_parse_init(cli_and_handlers):
    """Tests that the 'init' command is parsed correctly

    Args:
        cli (Cli): Command line parser class
    """
    def handle_init(args):
        assert args.command == 'init'
        assert args.force

    cli, handlers = cli_and_handlers

    # Set handlers
    handlers['init'] = handle_init

    # Run test
    cli.parse(["init", "--force"])
    cli.parse(["init", "-f"])


def test_parse_report(cli_and_handlers):
    """Tests that the report command is parsed correctly

    Args:
        cli (Cli): Command line parser class
    """
    template = "release-note"
    query = "repo:github/opensource.guide is:open"

    def handle_report(args):
        assert args.command == 'report'
        assert args.internal == template
        assert args.query == query

    cli, handlers = cli_and_handlers

    # Set handlers
    handlers['report'] = handle_report

    # Run test
    cli.parse(['report', '--internal', template, query])


def test_parse_report_failures(cli_and_handlers):
    cli, handlers = cli_and_handlers

    def handle_report(args):
        assert False, "Failures should not be handled"

    # Set handlers
    handlers['report'] = handle_report

    # Test username and password and config
    with pytest.raises(RuntimeError):
        cli.parse([
            'report', "repo:github/opensource.guide is:open",
            '--username', 'my_name',
            '--password', 'my_password',
            '--config', 'path/to/config'])

    # Test config exists
    with pytest.raises(RuntimeError):
        cli.parse([
            'report', "repo:github/opensource.guide is:open",
            '--config', 'path/to/config'])

    # Test template exists
    with pytest.raises(RuntimeError):
        cli.parse([
            'report', "repo:github/opensource.guide is:open",
            '--external', 'path/to/template'])


def test_list(cli_and_handlers):
    """Tests that the list command is parsed correctly

    Args:
        cli_and_handlers (dict): Description
    """
    def handle_list(args):
        assert args.command == 'list'

    cli, handlers = cli_and_handlers

    # Set handlers
    handlers['list'] = handle_list

    # Run test
    cli.parse(['list'])
