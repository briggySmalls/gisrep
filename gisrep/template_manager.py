"""Abstraction of jinja2 template management
"""

from abc import ABC
import importlib.util

import jinja2

from .errors import GisrepError

_TEMPLATE_ARGS = {
    'trim_blocks': True,
    'lstrip_blocks': True,
    'autoescape': jinja2.select_autoescape(['html', 'xml'])
}


class GisrepTemplate(ABC):
    """Abstract gisrep template

    Attributes:
        template (jinja2.Template): Template to wrap
    """

    def __init__(self, template):
        self.template = template

    def render(self, issues):
        return self.template.render(self.get_context(issues))

    @staticmethod
    def get_context(issues):
        return {'issues': issues}


class DefaultTemplate(GisrepTemplate):

    def __init__(self, template_string):
        """Jinja2 template wrapper created from a string

        Args:
            template_string (str): String to create template from
        """

        # Create a Jinja2 template from a string
        template = jinja2.Template(template_string, **_TEMPLATE_ARGS)
        super().__init__(template)


class FileTemplate(GisrepTemplate):
    def __init__(self, path):
        # Record the path
        self.path = path

        # Create a template loader
        loader = jinja2.FileSystemLoader(str(path.parent))

        # Create a Jinja2 environment
        env = jinja2.Environment(
            loader=loader,
            **_TEMPLATE_ARGS)

        try:
            # Return the template
            template = env.get_template(path.name)
        except jinja2.exceptions.TemplateNotFound:
            raise GisrepError("Couldn't find template: {}".format(path.name))

        # Call parent constructor with template
        super().__init__(template)

    def get_context(self, issues):
        # Check if there is a corresponding python module
        module_path = self.path.with_suffix('.py')
        if not module_path.exists():
            return {'issues': issues}

        # Module defines get_context
        module = FileTemplate.import_module(module_path)
        return module.get_context(issues)

    @staticmethod
    def import_module(module_path):
        """Imports the specified module dynamically

        Args:
            module_path (str): The module path

        Returns:
            module: The module that was imported
        """

        try:
            # Python 3.5+
            spec = importlib.util.spec_from_file_location(
                module_path.name,
                str(module_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except AttributeError:
            # Python 3.4
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(  # pylint: disable=deprecated-method
                module_path.name,
                str(module_path)).load_module()
        return module


class TemplateManager(object):

    def __init__(self, default_template):
        # Record the default template
        self.default_template = DefaultTemplate(default_template)

    def generate(self, issues, template_path):
        # Get a Jinja2 template
        template = (FileTemplate(template_path) if
                    template_path is not None else
                    self.default_template)

        # Generate a report using the issues
        return template.render(issues)
