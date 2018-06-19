"""
Github requester
"""

from functools import wraps

from gitlab import Gitlab
import attr
import click

from .reporter import Reporter

DEFAULT_TEMPLATE = r"""{% for issue in issues %}
- {{ issue['title'] }} [#{{ issue['iid'] }}]
{% endfor %}"""


@attr.s()
class GitLabConfig(object):
    token = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s()
class GitLabQuery(object):
    project = attr.ib(type=str)
    milestone = attr.ib(type=str)


def pass_gitlab(f):
    @click.option(
        '--token',
        help="GitLab personal access token")
    @click.option(
        '--url',
        default="https://gitlab.com",
        help="GitLab instance URL")
    @click.option(
        '--project',
        help="GitLab project to filter issues by")
    @click.option(
        '--milestone',
        help="GitLab milestone to filter issues by")
    @wraps(f)
    def gitlab_options(*args, **kwargs):
        """Publish issues from a GitLab search query
        (see https://docs.gitlab.com/ee/user/search/)"""
        reporter = GitLabReporter(GitLabConfig(
            token=kwargs.pop('token'),
            url=kwargs.pop('url')))
        query = GitLabQuery(
            project=kwargs.pop('project'),
            milestone=kwargs.pop('milestone'))
        return f(reporter, query, *args, **kwargs)
    return gitlab_options


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
        manager = (
            self.api.projects.get(query.project)
            if query.project
            else self.api)
        issues = manager.issues.list()
        return issues if len(issues) > 0 else None
