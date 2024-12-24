# Using `sxolar` from the Command Line

The `sxolar` library can be used from the command line to search for arXiv entries and display the results in a
user-friendly format. This section provides an overview of how to use `sxolar` from the command line, including the
available options and usage examples.

## Installation

The command-line interface for `sxolar` is automatically installed when you install the `sxolar` library using `pip`.
If you haven't installed `sxolar` yet, you can do so by running the following command:

```bash
pip install sxolar
```

## Usage

The `sxolar` command-line interface provides a simple way to search for arXiv entries based on various criteria.
There are presently the following commands available:

- `sxolar query`: Search for arXiv entries based on a query.
- `sxolar summary`: Display a human-readable summary of an arXiv search.

### `sxolar query`

The `sxolar query` command allows you to search for arXiv entries based on a query. You can specify various search
criteria such as the title, author, abstract, and publication date. Here is an example of how to use the `sxolar search`

```bash
sxolar search --title "quantum computing" --max-results 5
```

In this example, we search for arXiv entries related to quantum computing and specify that we want a maximum of 5
results.
The next example shows more complicated usage of the `sxolar search` command:

```bash
sxolar search --title "quantum computing" \
  --author "John Doe" \
  --author "Jane Smith" \
  --trailing 100 \
  --max-results 50
```

In this example, we search for arXiv entries related to quantum computing that were authored by either John Doe or Jane
Smith,
and we specify that we want a maximum of 50 results. We also use the `--trailing` option to search for entries that were
published in the last 100 days.

!!! note "Post-Filtering and Increasing `max-results`"

    The `--trailing` option specifies the number of days from the current date to search for entries. For example,
    `--trailing 100` searches for entries published in the last 100 days. Because this filter occurs after the search 
    results are retrieved, it may decrease the number of results returned. In such cases, it is currently recommended 
    to increase the number of results, you can use the `--max-results` option.

### `sxolar summary`

The `sxolar summary` command allows you to display a human-readable summary of an arXiv search. You can specify the
search criteria and the number of results to display. 


!!! note "Summaries Require Config Files"

    The `sxolar summary` command requires a configuration file. The configuration file is a YAML file that specifies the
    a set of named summaries. Each summary is a collection of sections, where each section is a formatted
    query. Each section / query can have a title, author, abstract, and other search criteria. More detail on the
    format of the configuration file can be found in the [Configuration Files](config-files.md) docs.


Here is an example of how to use the `sxolar summary` command:

```bash
sxolar summary --config-file config.yaml --name MySummary
```

In this example, we display a summary of the search summary named `MySummary` from the configuration file `config.yaml`.
This configuration file should contain the search criteria for the query. An acceptable
config file for the example above would look like this:

```yaml
MySummary:
  - name: "Section 1"
    authors: ["Author A", "Author B"]
    alls: ["Topic X"]
```

This configuration file specifies a summary named `MySummary` with one section named `Section 1`. The section searches for
entries with authors `Author A` or `Author B` and topics `Topic X`.
