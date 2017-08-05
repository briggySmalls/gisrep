from jinja2 import Environment, FileSystemLoader, select_autoescape, exceptions
import os
from locate import Locator, Locatable


class TemplateManager(object):
    def __init__(self, template_dirs):
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

        # Render the template
        return template.render(issues=issues)

    def list(self):
        return self.env.list_templates()
