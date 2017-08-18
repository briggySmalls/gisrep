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
- An Output, defaulting to stdout, used to deliver the report 

The template component can be either a built-in template tag or a filepath to a custom template. More information on creating custom templates is discussed in the [dedicated templates readme](gisrep/templates/README.md).

The search query is passed to the [Github search API](https://developer.github.com/v3/search/#search-issues) to filter issues and pull requests. Read the Github guide on [searching issues and pull requests](https://help.github.com/articles/searching-issues-and-pull-requests/) for help constructing queries.

The output is a method of delivering the report, for example printing to the console or saving to a file. To specify an output other than the console, use the `--output` argument. For example to save to a file:

```
gisrep report simple_report repo:"twbs/bootstrap is:open label:feature" --output file output.txt
```

### Listing built-ins

Listing the available built-in templates or outputs uses the `list` subcommand.

To list the tags for built-in templates use the following command:

```
gisrep list templates
```

To list the tags for built-in outputs use the following command:

```
gisrep list outputs
```

### Credentials

The tool needs to be initialised with Github credentials in order to access private repositories. The tool is initialised with the following command:

```
gisrep init
```

You will be prompted for your Github username and password. The password is stored in your system's password manager using [keyring](https://pypi.python.org/pypi/keyring). To overrwrite an existing configuration use the `--force` argument.