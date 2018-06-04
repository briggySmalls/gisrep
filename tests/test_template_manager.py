"""
Tests for the template_manager module
"""

import inspect
from pathlib import Path

import pytest

from gisrep.errors import GisrepError
from gisrep.template_manager import (
    DefaultTemplate, FileTemplate, TemplateManager)

SIMPLE_TEMPLATE_STRING = (
    r"{% for issue in issues %}{{ issue.number }}{% endfor %}")

EXTRA_CONTEXT_TEMPLATE_STRING = (
    SIMPLE_TEMPLATE_STRING +
    r"{{ extra_content }}")

SIMPLE_ISSUES = [
    {'title': "Issue 1", 'number': 1},
    {'title': "Issue 2", 'number': 2},
    {'title': "Issue 3", 'number': 3},
]


def get_context(issues):
    return {
        'issues': issues,
        'extra_content': 'hi'
    }


@pytest.fixture
def template_file(request, tmpdir):
    template_string, context_function = request.param

    # Create the template file
    FILENAME = "test_template.md"
    template_file = tmpdir.join(FILENAME + '.tplt')
    template_file.write(template_string)

    # Create the context file (if present)
    if context_function is not None:
        context_file = tmpdir.join(FILENAME + '.py')
        context_file.write(inspect.getsource(context_function))

    return Path(str(template_file))


@pytest.mark.parametrize(
    ['template_string', 'issues', 'expected_report'],
    [
        (SIMPLE_TEMPLATE_STRING, SIMPLE_ISSUES, '123')
    ]
)
def test_default_template(template_string, issues, expected_report):
    # Create the template
    template = DefaultTemplate(template_string)

    # Render a report
    report = template.render(issues)

    # Assert
    assert report == expected_report


@pytest.mark.parametrize(
    ['template_file', 'issues', 'expected_report'],
    [
        ((EXTRA_CONTEXT_TEMPLATE_STRING, get_context), SIMPLE_ISSUES, '123hi')
    ],
    indirect=['template_file']
)
def test_file_template(template_file, issues, expected_report):
    # Create the template
    template = FileTemplate(template_file)

    # Render a report
    report = template.render(issues)

    # Assert
    assert report == expected_report
