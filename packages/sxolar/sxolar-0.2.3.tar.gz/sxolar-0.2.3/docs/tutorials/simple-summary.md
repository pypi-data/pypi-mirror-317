# Tutorial: Simple Summary

This tutorial demonstrates how to generate a simple summary of search results using the `sxolar` library. Summaries
provide a concise overview of search results, including key metadata such as titles, authors, and abstracts. Users can
customize the content and format of summaries to suit their needs, making it easier to review and analyze search
results.
We first begin by setting up a configuration file that details the structure of the summary. Each
summary is a collection of sections, where each section represents a specific search query. Each section can have a
title, author, abstract, and other search criteria. The configuration file is a YAML file that specifies the named
summaries and their corresponding sections.

## Installation

If you have already installed the `sxolar` library, you can skip this step. Otherwise, you can install the library
using `pip` by running the following command:

```bash
pip install sxolar
```

## Configuration File

To generate a summary, you need to create a configuration file that specifies the structure of the summary. The
configuration file should be in the YAML format and contain the named summaries and their corresponding sections. Each
section can include search criteria such as title, author, abstract, and other metadata fields.

Example configuration file (`summary.yaml`):

```yaml
summary name 1:
  - name: "Section 1: Topic A x Authors 1, 2 | Recent 2 Weeks"
    authors: ["Author 1", "Author 2"]
    alls: ["Topic A"]
    trailing:
      num: 14
      unit: "days"

  - name: "Section 2: Topic B x Authors 3, 4 | Recent 2 Months"
    authors: ["Author 3", "Author 4"]
    alls: ["Topic B"]
    trailing:
      num: 2
      unit: "months"

summary name 2:
  - name: "Section 1: Topic C x Authors 5, 6"
    authors: ["Author 5", "Author 6"]
    alls: ["Topic C"]
```

In the above example, we define two named summaries, each with multiple sections. Each section specifies the search
criteria for the summary, including the title, authors, and other metadata fields. The `trailing` field specifies the
time frame for the search results, such as the past 2 weeks or 2 months.

## Generate Summary

Once you have created the configuration file, you can generate a summary using the `sxolar` library. The 
summary can be generated using the python library or the command line.

### Python Library

To generate a summary using the `sxolar` library, you can use the `sxolar.Config` class to read
and parse the `Summary` objects. Then the `Summary` objects can be used to generate the content summary.

Here is an example of how to generate a summary using the `sxolar` library:
This example will use the summary file contained in the repo at `./sample.yml`.

```{.python notest}
from sxolar import Config, Summary

# Load the configuration file, this will also parse the summary objects
config = Config("summary.yaml")

# Get the summary object for "summary name 1"
s1 = config.summaries("summary name 1")
assert isinstance(s1, Summary)

# Generate the summary first by refreshing the query
s1.refresh()

# Print the summary (plain)
print(s1.to_text())

# Print the summary (html, usually for email)
print(s1.to_html())
```

