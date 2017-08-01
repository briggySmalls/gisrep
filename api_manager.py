

class ApiManager(object):
    def __init__(self, username, password):
        # TODO: Implement
        print("ApiManager(username={0}, password={1}".format(
            username, password))

    def issues(self, repo, milestone=None, labels=None):
        print("issues(repo={0}, milestone={1}, labels={2}".format(
            repo, milestone, labels))
