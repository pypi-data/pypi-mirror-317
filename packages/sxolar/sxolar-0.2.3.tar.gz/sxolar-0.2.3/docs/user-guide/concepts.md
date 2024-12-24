# Key Concepts

The `sxolar` library provides two main interfaces for interacting with the arXiv API: a low-level interface and a
high-level interface. These interfaces are designed to cater to different user needs and preferences, offering varying
levels of control and abstraction. Throughout, there are core concepts that drive the design and functionality of the
`sxolar` library. These concepts are essential to understanding how the library works and how to use it effectively.
This page provides an overview of the key concepts that underpin the `sxolar` library, including search queries, search
results, and entry objects. Understanding these concepts will help you navigate
the library's documentation and use its features effectively.

## ArXiv API

The `sxolar` library interacts with the arXiv API to search for and retrieve arXiv entries. The arXiv API is a web-based
interface that allows users to access the arXiv repository programmatically. It provides a range of search and retrieval
capabilities, enabling users to find arXiv entries based on various criteria such as title, author, abstract, and
publication date. The `sxolar` library abstracts away the complexities of interacting with the arXiv API, providing a
user-friendly interface for searching and retrieving arXiv entries.

## Search Structure: Fields and Operators

The arXiv API uses a structured query language to search for entries in the arXiv repository. This query language allows
users to specify search criteria and logical combinations to filter the results.

Each query is composed of one or more **fields**, such as title, author, abstract, and category. 
Search fields are combined with **logical operators** like `AND`, `OR`, and `NOT`. 
By constructing valid search queries, users can retrieve specific subsets of arXiv entries that
match their criteria. For more detail on the arxiv API, see
the [arXiv API documentation](https://arxiv.org/help/api/user-manual).

The `sxolar` library provides classes and functions that help users construct valid search queries and submit them to
the arXiv API. By leveraging these abstractions, users can easily create complex search queries without needing to
understand the underlying query language of the arXiv API.

## Data Structure: Entries

The primary data structure internal to arXiv is the **entry** object. An entry object represents a single arXiv entry
and contains metadata such as the title, authors, abstract, publication date, and other relevant information. When
searching for arXiv entries, the arXiv API returns a collection of entries (formatted in XML) that match 
the search criteria _to the best of its ability_. 

The `sxolar` library parses these XML entries into Python objects.

## Search Results and Limitations

When a search query is submitted to the arXiv API, the API returns a list of entries that match the search criteria. 
These entries are considered search results and are represented as a collection of entry objects. The number of search
results returned by the API may be limited by the API itself, and users can specify the maximum number of results they
want to retrieve.

Often, the search results include entries that are not directly related to the search query but are considered 
relevant by the arXiv API. `sxolar` provides methods to filter and sort search results based on user-defined criteria,
but this sorting is done _after_ the search results are retrieved from the API. For example, 
users can post-filter search results based on publication date, and exact author name matches.

## Summaries and Sections

The `sxolar` library provides a range of features to help users interact with arXiv entries more effectively. One such
feature is the ability to generate human-readable summaries of search results. Summaries provide a concise overview of
the search results, including key metadata such as titles, authors, and abstracts. Users can customize the content and
format of summaries to suit their needs, making it easier to review and analyze search results.

A `Summary` is a collection of `Section` objects, each of which represents a specific configured query. Query
configuration and summary configuration can be stored in YAML formatted files. This allows `sxolar` to server
as a persisted search tool, where users can save and re-run complex search queries. For more
information on summaries and sections, see the [Configuration Files](config-files.md) documentation.

