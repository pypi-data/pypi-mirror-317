# Tutorial: Simple Query

This tutorial demonstrates how to use the `sxolar` library to search for arXiv entries based on a query. We will cover
the basic usage of the `sxolar` library and show how to search for arXiv entries using various criteria such as the
title, author, abstract, and publication date.

In this tutorial we want to search arXiv for entries related to quantum computing. We will search for entries that have
"quantum computing" in the title and display the top 5 results.

## Installation

If you have already installed the `sxolar` library, you can skip this step. Otherwise, you can install the library
using `pip` by running the following command:

```bash
pip install sxolar
```

## Basic Query

To search for arXiv entries based on a query, you can use the `sxolar.Query` api.
The `sxolar.Query` class provides a simple way to construct a query and retrieve search results.

Here is an example of how to search for arXiv entries related to quantum computing:

```python
from sxolar import Title

# Create a query object
query = Title("quantum computing")

# Execute the query and display the top 5 results
results = query.search(max_results=5)

# Display the search results
for result in results:
    print(result.title)
    print(result.author)
    print(result.summary)
    print()
```

In this example, we create a `Title` query object with the search term "quantum computing". We then execute the query
and display the top 5 results. The search results include the title, authors, and abstract of each entry.

You can customize the query by specifying additional search criteria such as author, abstract, and publication date.

## Advanced Query

You can construct more complex queries by combining multiple search criteria. For example, you can search for entries
related to quantum computing that were authored by a specific author and published within a specific time frame.

Here is an example of a more complex query:

```python
import datetime
from sxolar import Title, Author

# Create a query object with multiple search criteria
query = Title("quantum computing")
query &= (Author("John Doe") | Author("Jane Smith")).wrap()

# Execute the query and display the top 5 results
results = query.search(
    max_results=5,
    min_date=datetime.datetime(2022, 1, 1, tzinfo=datetime.UTC),
    max_date=datetime.datetime(2022, 12, 31, tzinfo=datetime.UTC),
)

# Display the search results
for result in results:
    print(result.title)
    print(result.author)
    print(result.summary)
    print()
```

In this example, we create a `Title` query object with the search term "quantum computing" and an `Author` query object
with the author names "John Doe" and "Jane Smith". We then combine the two query objects using logical operators to
create a complex query. We also specify the publication date range for the search results.

## Conclusion

This tutorial has demonstrated how to use the `sxolar` library to search for arXiv entries based on a query. You can
construct simple or complex queries by specifying various search criteria and logical combinations. The `sxolar` library
provides a user-friendly interface for searching and retrieving arXiv entries, making it easy to find relevant research
papers on arXiv.
