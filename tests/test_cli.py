"""
Tests for the Cli object
"""

import pytest

from gisrep.cli import Cli
from gisrep.errors import GisrepError


def default_handler(args):
    """Default handler for CLI callbacks

    Args:
        args (argparse.Namespace): Command line arguments
    """
    assert False, ("Default handler called with args: {0}".format(args))


@pytest.fixture
def handlers():
    """Fixture for providing Cli handlers

    Returns:
        dict: command-to-handler lookup
    """
    return {
        'init': default_handler,
        'report': default_handler,
        'list': default_handler,
    }


@pytest.fixture
def cli(handlers):  # pylint: disable=redefined-outer-name
    """Fixture for providing a Cli object

    Args:
        handlers (dict): Handlers for the Cli commands

    Returns:
        Cli: Cli object for testing
    """
    return Cli({
        'init': lambda args: (  # pylint: disable=unnecessary-lambda
            handlers['init'](args)),
        'report': lambda args: (  # pylint: disable=unnecessary-lambda
            handlers['report'](args)),
        'list': lambda args: (  # pylint: disable=unnecessary-lambda
            handlers['list'](args))
    })


def test_parse_init(cli, handlers):  # pylint: disable=redefined-outer-name
    """Tests that the 'init' command is parsed correctly

    Args:
        cli_and_handlers (tuple): Cli object and handler dict
    """
    def handle_init(args):
        """Handler for init function call

        Args:
            args (argparse.Namespace): Arguments from command line
        """
        assert args.command == 'init'
        assert args.force

    # Set handlers
    handlers['init'] = handle_init

    # Run test
    cli.parse(["init", "--force"])
    cli.parse(["init", "-f"])


def test_parse_report(cli, handlers):  # pylint: disable=redefined-outer-name
    """Tests that the report command is parsed correctly

    Args:
        cli_and_handlers (tuple): Cli object and handler dict
    """
    template = "release-note"
    query = "repo:github/opensource.guide is:open"

    def handle_report(args):
        """Handler for report function call

        Args:
            args (argparse.Namespace): Arguments from command line
        """
        assert args.command == 'report'
        assert args.internal == template
        assert args.query == query

    # Set handlers
    handlers['report'] = handle_report

    # Run test
    cli.parse(['report', '--internal', template, query])


def test_parse_report_failures(
        cli, handlers):  # pylint: disable=redefined-outer-name
    """Tests that the report command throws an error for invalid arguments

    Args:
        cli_and_handlers (tuple): Cli object and handler dict
    """

    def handle_report(args):  # pylint: disable=unused-argument
        """Handler for report function call

        Args:
            args (argparse.Namespace): Command line arguments
        """
        assert False, "Failures should not be handled"

    # Set handlers
    handlers['report'] = handle_report

    # Test username and password and config
    with pytest.raises(GisrepError):
        cli.parse([
            'report', "repo:github/opensource.guide is:open",
            '--username', 'my_name',
            '--password', 'my_password',
            '--config', 'path/to/config'])

    # Test config exists
    with pytest.raises(GisrepError):
        cli.parse([
            'report', "repo:github/opensource.guide is:open",
            '--config', 'path/to/config'])

    # Test template exists
    with pytest.raises(GisrepError):
        cli.parse([
            'report', "repo:github/opensource.guide is:open",
            '--external', 'path/to/template'])


def test_list(cli, handlers):  # pylint: disable=redefined-outer-name
    """Tests that the list command is parsed correctly

    Args:
        cli_and_handlers (tuple): Cli object and handler dict
    """
    def handle_list(args):
        """Handler for list function call

        Args:
            args (argparse.Namespace): Arguments from command line
        """
        assert args.command == 'list'

    # Set handlers
    handlers['list'] = handle_list

    # Run test
    cli.parse(['list'])
