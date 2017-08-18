# Gisrep

The open source Github issues reporter.

## Installation

```
pip install 'path/to/package'
```

This installs the `gisrep` script to the command line. 

## Usage

### Publishing reports

Publishing reports uses the `report` subcommand. For example to publish a report for all open issues in the bootstrap repo with the 'feature' label, using the 'simple_report' template, printed to the console:

```
gisrep report simple_report "repo:twbs/bootstrap is:open label:feature"
```

The gisrep report subcommand comprises three components:

- A Template `simple_report` to format issues
- A Github search query `"repo:twbs/..."` to filter issues
- An Output, defaulting to stdout, to present the report 

The template is a [jinja2](http://jinja.pocoo.org/docs/2.9/) template (and possibly some support logic) that formats the issues returned by the search query into a nice report.

The search query is passed to the [Github search API](https://developer.github.com/v3/search/#search-issues) using [PyGithub](https://github.com/PyGithub/PyGithub) to filter issues and pull requests. Read the Github guide on [searching issues and pull requests](https://help.github.com/articles/searching-issues-and-pull-requests/) for help constructing queries.

The output is a method of delivering the report. For example printing to the console or saving to a file.

To specify an output other than the console, use the `--output` argument. For example to save to a file:

```
gisrep report simple_report repo:"twbs/bootstrap is:open label:feature" --output file output.txt
```

### Templates

List the available templates with the following command:

```
gisrep templates list
```

The tags displayed can be used with the template positional argument to the `report` command.

The project is designed for the community to contribute useful templates meaning the tool should come with a useful collection of generic templates. However there may be a need for extending the tool with custom templates.

### Outputs

List the available outputs with the following command:

```
gisrep outputs list
```

The tags displayed can be used with the `--output` argument to the `report` subcommand.

### Credentials

The tool needs to be initialised with Github credentials in order to access private repositories. The tool is initialised with the following command:

```
gisrep init
```

You will be prompted for your Github username and password. The password is stored in your system's password manager using [keyring](https://pypi.python.org/pypi/keyring).