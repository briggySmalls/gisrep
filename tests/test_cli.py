import unittest
from cli import Cli


class TestCli(unittest.TestCase):
    def setUp(self):
        # Reset handlers to default
        self.handlers = {}
        self.handlers['init'] = self.default_handler
        self.handlers['report'] = self.default_handler
        self.handlers['templates'] = self.default_handler
        self.handlers['outputs'] = self.default_handler

        # Instantiate new Cli object
        self.cli = Cli({
            'init': lambda args : self.handlers['init'](args),
            'report': lambda args : self.handlers['report'](args),
            'templates': lambda args : self.handlers['templates'](args),
            'outputs': lambda args : self.handlers['outputs'](args),
        })

    def test_parse_init(self):
        def handle_init(args):
            self.assertTrue(args.force)

        # Set handlers
        self.handlers['init'] = handle_init

        # Run test
        self.cli.parse(["init", "--force"])
        self.cli.parse(["init", "-f"])

    def test_parse_report(self):
        template = "release-note"
        query = "repo:github/opensource.guide is:open"

        def handle_report(args):
            self.assertEqual(args.template, template)
            self.assertEqual(args.query, query)

        # Set handlers
        self.handlers['report'] = handle_report

        # Run test
        self.cli.parse([
            'report',
            template,
            query])

    def default_handler(self, args):
        self.fail("Default handler called with args: {0}".format(
            args))
