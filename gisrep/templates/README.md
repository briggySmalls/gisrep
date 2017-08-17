# Templates

Templates used by gisrep are simple text files, formatted in the [Jinja template syntax](http://jinja2.readthedocs.io/en/latest/templates.html), denoted by a .tplt extension.

## Custom templates

Custom templates can be passed to gisrep to publish specialised reports. By default, all that is required is to create a file that:

- Has the `.tplt` extension
- Is formatted in the [Jinja template syntax](http://jinja2.readthedocs.io/en/latest/templates.html)
- Accesses the `issues` context variable - a list of [PyGithub issue objects](http://pygithub.readthedocs.io/en/latest/github_objects/Issue.html)

For clarity gisrep templates should also contain an extension that hints at the format of any output document. For example a template 'report' that produces html should be named `report.html.tplt`.

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

Github search queries coupled with Jinja templating syntax, with its control structures, expressions, filters, etc. is sufficient to produce most reports. However sometimes it is necessary to perform some logic prior to formatting the results in the template.

In such cases it is possible to provide custom logic captured in python file that:

- Is in the same directory as the template
- Has the same file name as the template, but has the '\*.py' extension
- Contains a function `get_context(issues)` that returns a dictionary of variable names and their values

A simple example logic file, `report.md.py` is shown below:

```python
def get_context(issues):
    all_labels = set()
    for issue in issues:
        for label in issue.labels:
            all_labels.add(label)
    
    return {'issues': issues, 'labels': all_labels}
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