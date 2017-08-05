def get_context(issues):
    labels = []
    for issue in issues:
        for label in issue.labels:
            if label not in labels:
                labels.append(label)
                
    return {
        'all_labels': labels,
        'issues': issues
    }
