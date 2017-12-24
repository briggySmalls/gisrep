"""Context function for list_by_labels.html.tplt

Adds all_labels context
"""


def get_context(issues):
    """Adds the all_labels list of labels

    Args:
        issues (list): List of github.Issue.Issue objects

    Returns:
        dict: Context dictionary passed to list_by_labels.html.tplt template
    """
    labels = []
    unlabelled = []
    for issue in issues:
        if not issue.labels:
            unlabelled.append(issue)
        else:
            labels.extend([l for l in issue.labels if l not in labels])

    return {
        'labels': labels,
        'issues': issues,
        'unlabelled': unlabelled,
    }
