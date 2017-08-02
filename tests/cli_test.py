import unittest
from cli import Cli


class TestCli(unittest.TestCase):

    def test_parse_init(self):
        def handle_init(args):
            self.assertTrue(args.force)

        def handle_report(args):
            self.fail("Report should not be called")

        cli = Cli(handle_init, handle_report)
        cli.parse(["init", "--force"])
        cli.parse(["init", "-f"])

    def test_parse_report(self):
        template = "release-note"
        query = "repo:github/opensource.guide is:open"

        def handle_init(args):
            self.fail("Init should not be called")

        def handle_report(args):
            self.assertEqual(args.template, template)
            self.assertEqual(args.query, query)

        cli = Cli(handle_init, handle_report)
        cli.parse([
            'report',
            template,
            '--query', query])
