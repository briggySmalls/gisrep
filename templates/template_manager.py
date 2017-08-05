from locate import Locator, Locatable
from jinja2 import Environment, FileSystemLoader, select_autoescape, exceptions
import os
from abc import ABCMeta, abstractmethod
import importlib.util

TEMPLATE_EXTENSION = 'tplt'


class AbstractTemplate(object, metaclass=ABCMeta):
    def __init__(self):
        path, filename = os.path.split(
        )
        self.template_filename = filename
        self.template_path = path or './'

    def generate(self, issues):
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(FILEPATH)
        ).get_template(self.template_filename).render(self.get_context(issues))

    def get_context(self, issues):
        return issues


class TemplateManager(object):
    def __init__(self, template_dirs):
        # Create the template environment
        self.env = Environment(
            loader=FileSystemLoader(template_dirs),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, template, issues):
        # Load the template
        try:
            template = self.env.get_template(template)
        except exceptions.TemplateNotFound as exc:
            raise RuntimeError("Template does not exist") from exc

        # Check if corresponding module
        module_path = os.path.splitext(template.filename)[0] + '.py'
        context = {'issues': issues}
        if os.path.exists(module_path):
            # Module defines get_context
            module = self._import_module(module_path)
            context = module.get_context(issues)

        # Render the template
        return template.render(context)

    def list(self):
        # Get 
        self.env.list_templates(
            extensions=[TEMPLATE_EXTENSION])

    def _import_module(self, module_path):
        module_name = os.path.basename(module_path)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
