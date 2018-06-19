"""
Github requester
"""
from functools import wraps

from github import Github
import attr
import click

from .reporter import Reporter

# Template to default to if no custom template is provided
_DEFAULT_TEMPLATE = r"""{% for issue in issues %}
- {{ issue.title }} [#{{ issue.number }}]
{% endfor %}"""


@attr.s()
class GithubConfig(object):
    username = attr.ib(type=str)
    password = attr.ib(type=str)

    def has_credentials(self):
        return self.username is not None and self.password is not None


@attr.s()
class GithubQuery(object):
    search_string = attr.ib(type=str)


def pass_github(f):
    @click.option('--username', help="Github username")
    @click.option('--password', help="Github password")
    @click.argument('search')
    @wraps(f)
    def gitlab_options(*args, **kwargs):
        """Publish issues from a GitLab search query
        (see https://docs.gitlab.com/ee/user/search/)"""
        reporter = GithubReporter(
            GithubConfig(
                username=kwargs.pop('username'),
                password=kwargs.pop('password')))
        query = GithubQuery(
            search_string=kwargs.pop('search'))
        return f(reporter, query, *args, **kwargs)
    return gitlab_options


class GithubReporter(Reporter):
    NAME = "github"

    def __init__(self, config):
        # Create PyGithub API object
        if config.has_credentials():
            self.api = Github(
                config.username,
                config.password)
        else:
            self.api = Github()

        # Call Reporter initialiser
        super().__init__(_DEFAULT_TEMPLATE)

    @staticmethod
    def create_config(**kwargs):
        return GithubConfig(**kwargs)

    def _request(self, query):
        """ Request the issues """
        issues = self.api.search_issues(query.search_string, sort="created", order="asc")
        return issues if issues.get_page(0) else None
