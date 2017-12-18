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
    for issue in issues:
        for label in issue.labels:
            if label not in labels:
                labels.append(label)

    return {
        'all_labels': labels,
        'issues': issues
    }
