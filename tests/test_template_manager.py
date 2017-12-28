import os

from gisrep.templates.template_manager import (
    InternalTemplateManager, ExternalTemplateManager)

import pytest

TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "test_data")
EXTERNAL_TEMPLATE_TAG = "test_template"
INTERNAL_TEMPLATE_TAG = "simple_report.md"
FAKE_ISSUES = [
    {'title': "Issue 1", 'number': 1},
    {'title': "Issue 2", 'number': 2},
    {'title': "Issue 3", 'number': 3},
]


@pytest.fixture
def external_manager():
    return ExternalTemplateManager(TEST_DATA_DIR)


@pytest.fixture
def internal_manager():
    return InternalTemplateManager()


def test_external(external_manager):
    report = external_manager.generate(
        EXTERNAL_TEMPLATE_TAG,
        FAKE_ISSUES)

    # Assert contents
    assert report is not None
    assert report == "123"


def test_internal(internal_manager):
    report = internal_manager.generate(
        INTERNAL_TEMPLATE_TAG,
        FAKE_ISSUES)

    # Assert contents
    assert report is not None
    # Check line length (note: there is a blank line at end)
    assert len(report.split('\n')) == len(FAKE_ISSUES) + 1


def test_list(external_manager):
    # Get a list of templates
    templates = external_manager.list()

    # Assert list
    assert len(templates) == 1
    assert 'test_template' in templates
