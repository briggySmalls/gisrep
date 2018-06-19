"""Abstract reporter class
"""
from abc import ABC, abstractmethod

from gisrep.errors import GisrepError
from gisrep.template_manager import TemplateManager


def create_reporter(reporter_name, **kwargs):
    """Find and instantiate the specified reporter """
    subclasses = _all_subclasses(Reporter)

    # Instantiate the one that matches the name
    for cls in subclasses:
        try:
            class_name = cls.NAME
        except AttributeError:
            raise GisrepError(
                "{} missing NAME attribute".format(cls))

        if class_name == reporter_name:
            return cls(cls.create_config(**kwargs))

    # Raise an error if none found
    raise GisrepError("Reporter '{}' not found".format(reporter_name))


def _all_subclasses(cls):
    """Recursively search for subclasses"""
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in _all_subclasses(c)])


class Reporter(ABC):
    """Abstract reporter class for generating reports from a query

    Attributes:
        template_manager (TemplateManager): Template manager
    """

    def __init__(self, default_template):
        """Instantiates a reporter

        Args:
            default_template (str): String defining a default template
        """
        # Create a template manager
        self.template_manager = TemplateManager(default_template)

    def generate_report(self, query, template=None):
        """Generates a report from the query object and template

        Args:
            query (TYPE): Query object (reporter specific)
            template (pathlib.Path, optional): Path to a template to use

        Returns:
            str: Report content

        Raises:
            GisrepError: No issues found
        """
        # Request the issues
        issues = self._request(query)

        # Check issues were found
        if issues is None:
            raise GisrepError("No matching issues found")

        return self.template_manager.generate(issues, template)

    @abstractmethod
    def _request(self, query):
        pass

    @staticmethod
    @abstractmethod
    def create_config(**kwargs):
        pass
