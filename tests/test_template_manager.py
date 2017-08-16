import unittest
from gisrep.templates.template_manager import TemplateManager
import pickle
import os

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
TEST_TEMPLATE_TAG = "test_template"
FAKE_ISSUES = [
    {'title': "Issue 1", 'number': 1},
    {'title': "Issue 2", 'number': 2},
    {'title': "Issue 3", 'number': 3},
]


class TestTemplateManager(unittest.TestCase):

    def setUp(self):
        self.builder = TemplateManager(TEST_DATA_DIR)

    def test_simple(self):
        report = self.builder.generate(
            TEST_TEMPLATE_TAG,
            FAKE_ISSUES)

        # Assert contents
        self.assertIsNotNone(report)
        self.assertEqual(report, "123")

    def test_list(self):
        # Get a list of templates
        templates = self.builder.list()

        # Assert list
        self.assertTrue(len(templates) == 1)
        self.assertIn('test_template', templates)
