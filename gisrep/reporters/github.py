"""
Github requester
"""

from github import Github
import attr

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
        issues = self.api.search_issues(query, sort="created", order="asc")
        return issues if issues.get_page(0) else None
