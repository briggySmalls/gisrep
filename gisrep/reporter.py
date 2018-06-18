"""Abstract reporter class
"""
from abc import ABC, abstractmethod

from .errors import GisrepError
from .template_manager import TemplateManager


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
    
    @staticmethod
    def create(client_name):
        # Get the client
        return Reporter._find_client(client_name)

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
    def _find_client(, client_name):
        # Find all implementing classed
        subclasses = ._all_subclasses(Reporter)

        # Instantiate the one that matches the name
        for cls in subclasses:
            if cls.name == client_name:
                return cls()

    @staticmethod
    def _all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)])
