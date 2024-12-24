# Low-Level `sxolar` Interface

Since the arXiv service provides a RESTful API, it is possible to interact with the arXiv service programmatically.
`sXolar` provides a low-level interface to the arXiv API, which allows users to interact with the arXiv service 
in a more natural way. At its core, the low-level interface is a set of functions that allow users to format
search query strings, submit search queries to arXiv in accordance with api constraints, 
and extract useful information from search results.

The low-level interface of sXolar provides a more direct way to interact with the arXiv API. This interface is more
flexible than the high-level interface, but requires more knowledge of the arXiv API.
The low-level interface is built from scratch and incorporates the latest features of the arXiv API. The low-level
interface is designed to be as user-friendly as possible, while still providing access to the full functionality of the
arXiv API.

## Core Components

The low-level interface consists of several core components:

- [`format_search_query`][sxolar.api.arxiv.format_search_query]: A function that takes pythonic 
    user inputs and formats them into a valid arXiv search query string. This function can accept
    information related to all search fields, including the title, author, abstract, and more. 
    Further, it can also accept information related to the logical operators, such as `AND`, `OR`, and `NOT`,
    when combining multiple search fields.
- [`Entry`][sxolar.api.arxiv.Entry]: Represents an arXiv entry, and is the primary
    object returned by the low-level interface. It has attributes for all the metadata 
    of an arXiv entry, including the title, authors, abstract, and more.
- [`execute`][sxolar.api.arxiv.execute]: A function that takes a formatted search query string and submits
    it to the arXiv API. This function returns a list of [`Entry`][sxolar.api.arxiv.Entry] objects, each of which
    represents an arXiv entry that matches the search query.
- [`query`][sxolar.api.arxiv.query]: A function that combines the functionality of `format_search_query` and `execute`.
    This function takes pythonic user inputs, formats them into a valid arXiv search query string, and submits the query
    to the arXiv API. This function returns a list of [`Entry`][sxolar.api.arxiv.Entry] objects, each of which represents
    an arXiv entry that matches the search query.

## Example Usage

Here is an example of how to use the low-level interface to search for arXiv entries:

```python
from sxolar.api.arxiv import query

# Search for arXiv entries related to quantum computing
entries = query(title='quantum computing', max_results=5)

for entry in entries:
    print(entry.title)
    print(entry.author)
    print(entry.summary)
```

In this example, we use the `query` function to search for arXiv entries related to quantum computing.
We specify that we want a maximum of 5 results, and then iterate over the results to print out the title, authors, and summary of each entry.

The low-level interface provides a powerful and flexible way to interact with the arXiv API, allowing users to search 
for and retrieve arXiv entries based on a wide range of criteria. This next example shows a more complex search query:

```python
import datetime
from sxolar.api.arxiv import query

# Search for arXiv entries related to quantum computing that were published in 2021
entries = query(
    title='quantum computing', 
    min_date=datetime.datetime(2021, 1, 1, tzinfo=datetime.UTC),
    max_date=datetime.datetime(2021, 12, 31, tzinfo=datetime.UTC),
    max_results=5,
)

for entry in entries:
    print(entry.title)
    print(entry.author)
    print(entry.summary)
```

!!! note "Max Results"
    
    The `max_results` parameter specifies the maximum number of results to return
    from the arxiv search query. However, the `sxolar` package can impose additional
    filters on the results after they have been returned from arxiv, leading to fewer
    results than specified by `max_results`. This is because the raw arxiv search 
    results often contain duplicates or entries that do not meet the criteria specified
    by the user. In the example above, we specify that we want a maximum of 5 results,
    but the actual number of results returned may be less than 5, since we are also
    filtering out entries that were not published in 2021. Future versions of the package
    may provide more control over this behavior.
    
    
