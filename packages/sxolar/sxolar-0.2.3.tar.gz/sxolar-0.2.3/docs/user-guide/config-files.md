# Configuration Files

The `sxolar` command-line interface provides a simple way to search for arXiv entries based on various criteria. The
`sxolar summary` command allows you to display a human-readable summary of an arXiv search. The `sxolar summary` command
requires a configuration file. The configuration file is a YAML file that specifies a set of named queries. Each query
can have a title, author, abstract, and other search criteria.

## Structure of Configuration Files

Configuration files for `sxolar` are structured as follows:

- Each configuration file is a YAML file.
- The top-level keys in the YAML file are the names of the Summaries.
- Each Summary is a collection of Sections.
- Each Section is a collection of name and search criteria.

## Examples

Here are some examples of configuration files for `sxolar`.

### Simple Configuration File

Here is an example of a simple configuration file:

```yaml
MySummary:
  - name: "Section 1: John and Jane"
    authors: [
      "John Doe",
      "Jane Smith",
    ]
    max_results: 5

  - name: "Section 2: Quantum Computing"
    titles: [
      "quantum computing",
    ]
    max_results: 5
```

Note that the configuration file specifies a summary
named `MySummary` with two sections. The first section is named
`Section 1: John and Jane` and searches for entries authored by
"John Doe" and "Jane Smith". The second section is named
`Section 2: Quantum Computing` and searches for entries with the
title "quantum computing".

### Advanced Configuration File

Here is an example of a simple configuration file:

```yaml
MySummary2:
  - name: "Section 1: John and Jane Recent"
    authors: [
      "John Doe",
      "Jane Smith",
    ]
    max_results: 50
    trailing:
      num: 4
      unit: "weeks"

  - name: "Section 2: Quantum Computing & Multiverse"
    titles: [
      "quantum computing",
    ]
    alls: [
      "multiverse",
      "many worlds",
    ]
    alls_operator: " OR "
    max_results: 10
```

In this example, the configuration file specifies a summary named `MySummary2` with two sections. The first section is
named `Section 1: John and Jane Recent` and searches for entries authored by "John Doe" and "Jane Smith" within the last
4 weeks. The second section is named `Section 2: Quantum Computing & Multiverse` and searches for entries with the
title "quantum computing" and either "multiverse" or "many worlds" in any search field.
