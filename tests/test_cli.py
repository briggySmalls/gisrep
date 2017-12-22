import unittest
from gisrep.cli import Cli


class TestCli(unittest.TestCase):
    def setUp(self):
        # Reset handlers to default
        self.handlers = {}
        self.handlers['init'] = self.default_handler
        self.handlers['report'] = self.default_handler
        self.handlers['list'] = self.default_handler

        # Instantiate new Cli object
        self.cli = Cli({
            'init': lambda args: self.handlers['init'](args),
            'report': lambda args: self.handlers['report'](args),
            'list': lambda args: self.handlers['list'](args),
        })

    def test_parse_init(self):
        def handle_init(args):
            self.assertEqual(args.command, 'init')
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
            self.assertEqual(args.command, 'report')
            self.assertEqual(args.template, template)
            self.assertEqual(args.query, query)

        # Set handlers
        self.handlers['report'] = handle_report

        # Run test
        self.cli.parse(['report', '--template', template, query])

    def test_list_templates(self):
        def handle_list_templates(args):
            self.assertEqual(args.command, 'list')

        # Set handlers
        self.handlers['list'] = handle_list_templates

        # Run test
        self.cli.parse(['list'])

    def default_handler(self, args):
        self.fail("Default handler called with args: {0}".format(
            args))
