"""
Module that defines how templates are located
"""
import importlib.util
import os

from jinja2 import (
    Environment, FileSystemLoader, PackageLoader, exceptions,
    select_autoescape)

from ..errors import GisrepError

TEMPLATE_EXTENSION = 'tplt'


class TemplateManager(object):
    """
    Class for template manager. The template manager class locates templates
    used for generating reports

    Attributes:
        env (jinja2.Environment): Jinja2 templating environment

    """

    def __init__(self, loader):
        self.env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=select_autoescape(['html', 'xml']))

    def generate(self, filename, issues):
        """Generates a report

        Args:
            filename (str): The filename of the template to use
            issues (github.Issue.Issue): The issues to report

        Returns:
            str: The report

        Raises:
            RuntimeError: Template not found
        """

        # Load the template
        try:
            template = self.env.get_template(
                "{0}.{1}".format(filename, TEMPLATE_EXTENSION))
        except exceptions.TemplateNotFound:
            raise GisrepError("Couldn't find template: {}".format(filename))

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
        try:
            # Python 3.5+
            spec = importlib.util.spec_from_file_location(
                module_name,
                module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except AttributeError:
            # Python 3.4
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(  # pylint: disable=deprecated-method
                module_name,
                module_path).load_module()
        return module


class ExternalTemplateManager(TemplateManager):

    """Template manager that fetches user templates (external)
    """

    def __init__(self, template_path):
        # Create the template loader
        loader = FileSystemLoader(template_path)

        # Call the parent constructor with our loader
        super().__init__(loader)


class InternalTemplateManager(TemplateManager):

    """Template manager that fetches package templates (internal)
    """

    def __init__(self):
        # Create the template loader
        loader = PackageLoader('gisrep', 'templates')

        # Call the parent constructor with our loader
        super().__init__(loader)
