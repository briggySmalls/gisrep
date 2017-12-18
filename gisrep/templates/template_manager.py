"""
Module that defines how templates are located
"""
import importlib.util
import os

from jinja2 import Environment, FileSystemLoader, exceptions, select_autoescape

TEMPLATE_EXTENSION = 'tplt'
TOOL_TEMPLATE_DIR = os.path.dirname(os.path.realpath(__file__))


class TemplateManager(object):
    """
    Class for template manager. The template manager class locates templates
    used for generating reports

    Attributes:
        env (jinja2.Environment): Jinja2 templating environment

    """

    def __init__(self, template_dirs):

        # Create the template environment
        self.env = Environment(
            loader=FileSystemLoader(template_dirs),
            autoescape=select_autoescape(['html', 'xml']))

    def generate(self, template, issues):
        """Generates a report

        Args:
            template (str): The template to format the report
            issues (github.Issue.Issue): The issues to report

        Returns:
            str: The report

        Raises:
            RuntimeError: Template not found
        """

        # Load the template
        try:
            template = self.env.get_template(
                "{0}.{1}".format(template, TEMPLATE_EXTENSION))
        except exceptions.TemplateNotFound as exc:
            raise RuntimeError("Template does not exist") from exc

        # Check if corresponding module
        module_path = os.path.splitext(template.filename)[0] + '.py'
        context = {'issues': issues}
        if os.path.exists(module_path):
            # Module defines get_context
            module = TemplateManager.import_module(module_path)
            context = module.get_context(issues)

        # Render the template
        return template.render(context)

    def list(self):
        """Lists the available templates

        Returns:
            list: The tags of the available templates
        """

        # Get list of template files
        templates = self.env.list_templates(
            extensions=[TEMPLATE_EXTENSION])

        # Strip template from text
        for i, template in enumerate(templates):
            templates[i] = os.path.splitext(template)[0]

        return templates

    @staticmethod
    def import_module(module_path):
        """Imports the specified module dynamically

        Args:
            module_path (str): The module path

        Returns:
            module: The module that was imported
        """

        module_name = os.path.basename(module_path)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
