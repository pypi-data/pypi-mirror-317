# High-Level `sxolar` Interface

The high-level interface of `sxolar` provides a more simplified way to interact with the 
arXiv API. This interface is built on top of the [low-level interface](low-level.md) and 
provides a more user-friendly way to search for and retrieve arXiv entries. The high-level 
interface is designed to be easy to use and requires minimal knowledge of the arXiv API.

The high-level interface is essentially an object-oriented wrapper around the low-level
interface, providing a more intuitive way to specify search criteria and retrieve arXiv
entries. Search components are created as objects and combined using builtin logical operators
to create complex search queries. 

## Core Components

The high-level interface consists of several core components and methods:

- [`Query`][sxolar.api.search.Query]: A class that represents a search query for arXiv entries. 
    This class is a base class that accepts a fully formatted query. Field-specific subclasses
    provide a more object-oriented, user-friendly way to specify search criteria and logical
    combinations.
    - [`Title`][sxolar.api.search.Title]: A subclass of `Query` that represents the title field of an arXiv entry.
    - [`Author`][sxolar.api.search.Author]: A subclass of `Query` that represents the author field of an arXiv entry.
    - [`Abstract`][sxolar.api.search.Abstract]: A subclass of `Query` that represents the abstract field of an arXiv entry.
    - [`Category`][sxolar.api.search.Category]: A subclass of `Query` that represents the category field of an arXiv entry.
    - [`JournalRef`][sxolar.api.search.JournalRef]: A subclass of `Query` that represents the journal reference field of an arXiv entry.
    - [`All`][sxolar.api.search.All]: A subclass of `Query` that represents all fields of an arXiv entry.
- [`Query.search`][sxolar.api.search.Query.search]: A method that submits the search query to the arXiv API and returns a list 
    of [`Entry`][sxolar.api.arxiv.Entry] objects that match the query. This method accepts arguments for sorting, maximum results,
    and date filtering of results.

## Example Usage

Here is an example of how to use the high-level interface to search for arXiv entries:

```python
from sxolar.api.search import Title

# Create a search query for arXiv entries related to quantum computing
query = Title('quantum computing')

# Submit the search query and retrieve the results
entries = query.search(max_results=5)

for entry in entries:
    print(entry.title)
    print(entry.author)
    print(entry.summary)
```

In this example, we create a search query for arXiv entries related to quantum computing using the `Title` class.
We specify that we want a maximum of 5 results and then iterate over the results to print out the title, authors, 
and summary of each entry.

The high-level interface provides a more user-friendly way to interact with the arXiv API, allowing users to search
for and retrieve arXiv entries based on a wide range of criteria. This next example shows a more complex search query:

```python
import datetime
from sxolar.api.search import Title, Author

# Create a search query for arXiv entries related to quantum computing that were 
# published by either of two authors: John Doe or Jane Smith in 2021
query = Title('quantum computing') 
query &= (Author('John Doe') | Author('Jane Smith')).wrap()

# Submit the search query and retrieve the results
entries = query.search(min_date=datetime.datetime(2021, 1, 1, tzinfo=datetime.UTC), 
                       max_date=datetime.datetime(2021, 12, 31, tzinfo=datetime.UTC),
                       max_results=5)

for entry in entries:
    print(entry.title)
    print(entry.author)
    print(entry.summary)
```

In this example, we create a search query for arXiv entries related to quantum computing that were published by either
of two authors, John Doe or Jane Smith, in 2021. We specify that we want a maximum of 5 results and then iterate over
the results to print out the title, authors, and summary of each entry. The high-level interface allows for complex
search queries to be constructed using logical operators and field-specific classes. Note that in this example, we use
the `wrap` method to group the author queries together using parentheses to ensure the correct logical combination.



