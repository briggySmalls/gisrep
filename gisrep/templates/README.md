# Templates

Templates used by gisrep are text files formatted in the [Jinja template syntax](http://jinja2.readthedocs.io/en/latest/templates.html), denoted by a .tplt extension.

## Custom templates

Custom templates can be passed to gisrep to publish specialised reports. All that is required is to create a file that:

- Has the `.tplt` extension
- Is formatted in the [Jinja template syntax](http://jinja2.readthedocs.io/en/latest/templates.html)
- Accesses the `issues` context variable - a list of [PyGithub issue objects](http://pygithub.readthedocs.io/en/latest/github_objects/Issue.html)

Gisrep templates should contain an extension that hints at the format of any output document. For example a template 'report' that produces HTML should be named `report.html.tplt`.

A simple example template, `simple.md.tplt` is shown below:

```jinja2
{% for issue in issues %}
- {{ issue.title }} - ({{ issue.number }})
{% endfor %}
```

This template could then be passed to gisrep using the following example command:

```
gisrep report ./simple.md.tplt "repo:twbs/bootstrap"
```

## Custom logic

A Github search query coupled with Jinja's templating syntax (with its control structures, expressions, filters, etc.) is sufficient to produce most reports. However sometimes it is necessary to perform some logic prior to formatting the results in the template.

Custom logic can be supplied in python file that:

- Is in the same directory as the template
- Has the same file name as the template, but has the '\*.py' extension
- Contains a function `get_context(issues)` that returns a dictionary of variable names and their values

A simple example logic file, `report.md.py` is shown below:

```python
def get_context(issues):
    labels = []
    for issue in issues:
        labels.extend([l for l in issue.labels if l not in labels])

    return {
        'labels': labels,
        'issues': issues
    }
```

The corresponding template file, `report.md.tplt`, might look like:

```
{% for label in labels %}
	# {{ label.name }}
	{% for issue in issues %}
		{% if label in issue.labels %}
- {{ issue.title }} - ({{ issue.number }})
		{% endif %}
	{% endfor %}
{% endfor %}
```