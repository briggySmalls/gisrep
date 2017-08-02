import unittest
from template_manager import TemplateManager


TEST_ISSUES = [
    { 'title': "My first", 'number': 1},
    { 'title': "My second", 'number': 2},
]


class TestTemplateManager(unittest.TestCase):

    def setUp(self):
        self.builder = TemplateManager()

    def test_simple(self):
        report = self.builder.generate(
            'simple_report.txt',
            TEST_ISSUES)

        self.assertIsNotNone(report)
        print(report)
