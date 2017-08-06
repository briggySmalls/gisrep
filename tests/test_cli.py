import unittest
from cli import Cli


class TestCli(unittest.TestCase):
    def setUp(self):
        # Reset handlers to default
        self.handlers = {}
        self.handlers['init'] = self.default_handler
        self.handlers['report'] = self.default_handler
        self.handlers['list_templates'] = self.default_handler
        self.handlers['list_outputs'] = self.default_handler

        # Instantiate new Cli object
        self.cli = Cli({
            'init': lambda args : self.handlers['init'](args),
            'report': lambda args : self.handlers['report'](args),
            'list_templates': lambda args : self.handlers['list_templates'](args),
            'list_outputs': lambda args : self.handlers['list_outputs'](args),
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
        self.cli.parse([
            'report',
            template,
            query])

    def test_list_templates(self):
        def handle_list_templates(args):
            self.assertEqual(args.command, 'list')
        
        # Set handlers
        self.handlers['list_templates'] = handle_list_templates

        # Run test
        self.cli.parse([
            'templates',
            'list'])

    def test_list_outputs(self):
        def handle_list_outputs(args):
            self.assertEqual(args.command, 'list')
        
        # Set handlers
        self.handlers['list_outputs'] = handle_list_outputs

        # Run test
        self.cli.parse([
            'outputs',
            'list'])

    def default_handler(self, args):
        self.fail("Default handler called with args: {0}".format(
            args))
