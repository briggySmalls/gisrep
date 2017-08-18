CATEGORIES = ['enhancement', 'bug']

def get_context(issues):
    uncategorised = [issue for issue in issues if not any(label.name in CATEGORIES for label in issue.labels)]
    return {'issues': issues, 'uncategorised': uncategorised}
