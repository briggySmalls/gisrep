from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'templates')


class TemplateManager(object):
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, template, issues):
        # Load the template
        template = self.env.get_template(template)
        # Render the template
        return template.render(issues=issues)
