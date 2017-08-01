import unittest
from cli import Cli


class TestCli(unittest.TestCase):

    def test_parse_init(self):
        def handle_init(args):
            self.assertTrue(args.local)
            self.assertTrue(args.force)

        def handle_report(args):
            self.fail("Report should not be called")

        cli = Cli(handle_init, handle_report)
        cli.parse(["init", "--local", "--force"])
        cli.parse(["init", "-l", "-f"])

    def test_parse_report(self):
        template = "release-note"
        repo = "https://www.google.com"
        milestone = "My milestone"
        label_1 = "label_1"
        label_2 = "label_2"
        label_3 = "label_3"

        def handle_init(args):
            self.fail("Init should not be called")

        def handle_report(args):
            self.assertEqual(args.repo, repo)
            self.assertEqual(args.milestone, milestone)
            self.assertIn(label_1, args.labels)
            self.assertIn(label_2, args.labels)
            self.assertIn(label_3, args.labels)

        cli = Cli(handle_init, handle_report)
        cli.parse([
            'report',
            template,
            '--repo', repo,
            '--milestone', milestone,
            '--labels', label_1, label_2, label_3])
