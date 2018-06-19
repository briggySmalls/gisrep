"""
Github requester
"""

from gitlab import Gitlab
import attr

from .reporter import Reporter

DEFAULT_TEMPLATE = r"""{% for issue in issues %}
- {{ issue['title'] }} [#{{ issue['iid'] }}]
{% endfor %}"""


@attr.s()
class GitLabConfig(object):
    token = attr.ib(type=str)
    url = attr.ib(type=str)


class GitLabReporter(Reporter):
    NAME = "gitlab"

    def __init__(self, config):
        # Create GitLab API object
        self.api = Gitlab(
            config.url,
            private_token=config.token if config.token else None)

        # Call Reporter initialiser
        super().__init__(DEFAULT_TEMPLATE)

    @staticmethod
    def create_config(**kwargs):
        return GitLabConfig(**kwargs)

    def _request(self, query):
        """ Request the issues """
        issues = self.api.search('issues', query)
        return issues if len(issues) > 0 else None
