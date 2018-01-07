"""
Tests for the template_manager module
"""

import os

import pytest

from gisrep.errors import GisrepError
from gisrep.templates.template_manager import (
    ExternalTemplateManager, InternalTemplateManager)

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
    """Fixture for an ExternalTemplateManager

    Returns:
        ExternalTemplateManager: The template manager
    """
    return ExternalTemplateManager(TEST_DATA_DIR)


@pytest.fixture
def internal_manager():
    """Fixture for an InternalTemplateManager

    Returns:
        InternalTemplateManager: The template manager
    """
    return InternalTemplateManager()


def test_external(external_manager):  # pylint: disable=redefined-outer-name
    """Tests reporting with an external template

    Args:
        external_manager (ExternalTemplateManager): The template manager
    """
    report = external_manager.generate(
        EXTERNAL_TEMPLATE_TAG,
        FAKE_ISSUES)

    # Assert contents
    assert report is not None
    lines = report.split('\n')
    assert lines[0] == "123"
    assert lines[1] == "test"


def test_internal(internal_manager):  # pylint: disable=redefined-outer-name
    """Tests reporting with an external template

    Args:
        internal_manager (ExternalTemplateManager): The template manager
    """
    report = internal_manager.generate(
        INTERNAL_TEMPLATE_TAG,
        FAKE_ISSUES)

    # Assert contents
    assert report is not None
    # Check line length (note: there is a blank line at end)
    assert len(report.split('\n')) == len(FAKE_ISSUES) + 1


def test_missing_internal(
        internal_manager):  # pylint: disable=redefined-outer-name
    """Tests reporting with a non-existant internal template

    Args:
        internal_manager (InternalTemplateManager): The template manager
    """
    with pytest.raises(GisrepError):
        internal_manager.generate(
            'missing_report.md',
            FAKE_ISSUES)


def test_external_list(
        external_manager):  # pylint: disable=redefined-outer-name
    """Tests listing external templates

    Args:
        external_manager (ExternalTemplateManager): The template manager
    """
    assert_external_list(external_manager)


def test_internal_list(
        internal_manager):  # pylint: disable=redefined-outer-name
    """Tests listing internal templates

    Args:
        internal_manager (InternalTemplateManager): The template manager
    """
    assert_internal_list(internal_manager)


def assert_internal_list(manager):
    """Asserts the internal template list is correct

    Args:
        manager (InternalTemplateManager): The template manager
    """
    # Get a list of templates
    templates = manager.list()

    # Assert list
    assert len(templates) == 2
    assert 'simple_report.md' in templates
    assert 'list_by_labels.html' in templates


def assert_external_list(manager):
    """Asserts the external template list is correct

    Args:
        manager (ExternalTemplateManager): The template manager
    """
    # Get a list of templates
    templates = manager.list()

    # Assert list
    assert len(templates) == 1
    assert 'test_template' in templates
