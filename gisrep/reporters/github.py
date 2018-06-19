"""
Github requester
"""

from github import Github

from ..reporter import Reporter

# Template to default to if no custom template is provided
_DEFAULT_TEMPLATE = r"""{% for issue in issues %}
- {{ issue.title }} [#{{ issue.number }}]
{% endfor %}"""


class GithubReporter(Reporter):
    def __init__(self, credentials=None):
        # Create PyGithub API object
        if credentials is not None:
            self.api = Github(
                credentials['username'],
                credentials['password'])
        else:
            self.api = Github()

        # Call Reporter initialiser
        super().__init__(_DEFAULT_TEMPLATE)

    def name(self):
        return "github"

    def _request(self, query):
        """ Request the issues """
        issues = self.api.search_issues(query, sort="created", order="asc")
        return issues if issues.get_page(0) else None
