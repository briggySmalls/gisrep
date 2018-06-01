from .errors import GisrepError
from .template_manager import TemplateManager


class Reporter(object):

    def __init__(self, default_template_string):
        # Create a template manager
        self.template_manager = TemplateManager(default_template_string)

    def generate_report(self, query, template=None):
        # Request the issues
        issues = self._request(query)

        # Check issues were found
        if not issues.get_page(0):
            raise GisrepError("No matching issues found")

        return self.template_manager.generate(issues, template)
