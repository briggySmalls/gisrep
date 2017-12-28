import os

from gisrep.templates.template_manager import ExternalTemplateManager

import pytest

TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "test_data")
TEST_TEMPLATE_TAG = "test_template"
FAKE_ISSUES = [
    {'title': "Issue 1", 'number': 1},
    {'title': "Issue 2", 'number': 2},
    {'title': "Issue 3", 'number': 3},
]


@pytest.fixture
def external_manager():
    return ExternalTemplateManager(TEST_DATA_DIR)


def test_simple(external_manager):
    report = external_manager.generate(
        TEST_TEMPLATE_TAG,
        FAKE_ISSUES)

    # Assert contents
    assert report is not None
    assert report == "123"


def test_list(external_manager):
    # Get a list of templates
    templates = external_manager.list()

    # Assert list
    assert len(templates) == 1
    assert 'test_template' in templates
