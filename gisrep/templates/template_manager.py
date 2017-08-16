"""
Module that defines how templates are located
"""

from ..locate import Locator, Locatable
from jinja2 import Environment, FileSystemLoader, select_autoescape, exceptions
import os
from abc import ABCMeta, abstractmethod
import importlib.util

TEMPLATE_EXTENSION = 'tplt'
TOOL_TEMPLATE_DIR = os.path.dirname(os.path.realpath(__file__))

class AbstractTemplate(object, metaclass=ABCMeta):
    """
    Abstract class for template.
    
    """

    def __init__(self):
        path, filename = os.path.split(
        )
        self.template_filename = filename
        self.template_path = path or './'

    def generate(self, issues):
        """
        Generates a report from the issues
        
        :param      issues:  The issue objects to report
        :type       issues:  list
        
        :returns:   The report, formatted by the template
        :rtype:     string
        """

        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(FILEPATH)
        ).get_template(self.template_filename).render(self.get_context(issues))

    def get_context(self, issues):
        """
        Gets the context for the template
        
        :param      issues:  The issue objects to report
        :type       issues:  list
        
        :returns:   The context passed to the template
        :rtype:     dict
        """

        return issues


class TemplateManager(object):
    """
    Class for template manager. The template manager class locates templates
    used for generating reports

    """

    def __init__(self, template_dirs):

        # Create the template environment
        self.env = Environment(
            loader=FileSystemLoader(template_dirs),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, template, issues):
        """
        Generates a report
        
        :param      template:  The template to format the report
        :param      issues:    The issues to report
        :type       template:  string
        :type       issues:    list
        
        :returns:   The report
        :rtype:     string
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
            module = self.import_module(module_path)
            context = module.get_context(issues)

        # Render the template
        return template.render(context)

    def list(self):
        """
        Lists the available templates
                
        :returns:   The tags of the available templates
        :rtype:     list
        """

        # Get list of template files
        templates = self.env.list_templates(
            extensions=[TEMPLATE_EXTENSION])

        # Strip template from text
        for i in range(len(templates)):
            templates[i] = os.path.splitext(templates[i])[0]

        return templates

    def import_module(self, module_path):
        """
        Imports the specified module dynamically
        
        :param      module_path:  The module path
        :type       module_path:  string
        
        :returns:   The module that was imported
        :rtype:     module
        """

        module_name = os.path.basename(module_path)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
