from github import Github


class ApiManager(object):
    def __init__(self, username, password):
        self.client = Github(username, password)

    def get_issues(self, repo_url, milestone_id=None, label_ids=None):
        # Get the repo
        repo = self.client.get_repo(repo_url)

        # Get the milestone (if necessary)
        if milestone_id is not None:
            milestone = repo.get_milestone(milestone_id)

        # Get the label objects (if necessary)
        if label_ids is not None:
            labels = []
            for label_id in label_ids:
                labels.append(repo.get_label(label_id))

        # Request the issues
        return repo.get_issues(
            milestone=milestone,
            state="closed",
            labels=labels)
