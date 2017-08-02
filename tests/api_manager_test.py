import unittest
from api_manager import ApiManager

GITHUB_USERNAME = "briggySmalls"
GITHUB_TOKEN = "cda88c6356b350b32e729a490ea1c717a066a66f"
GITHUB_REPO = "entia/aptus-software"


class TestApiManager(unittest.TestCase):

    def test_get_all_issues(self):
        # Create api manager
        api = ApiManager(
            GITHUB_USERNAME,
            GITHUB_TOKEN)

        # Request all issues
        issues = api.get_issues(repo)

        # Make some simple assertions
        self.assertTrue(len(issues) > 0)
        
    def test_
