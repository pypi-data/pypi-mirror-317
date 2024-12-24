"""Arxiv API wrappers for sxolar, low-level functions for querying the Arxiv API.
For more user-friendly functions, see the `sxolar.api.query` module.

References:
    [1] API Basics: https://info.arxiv.org/help/api/basics.html
    [2] Rate Limits: https://info.arxiv.org/help/api/tou.html
    [3] Search Query Language: https://info.arxiv.org/help/api/user-manual.html
        #query_details
    [4] Entry output format: https://info.arxiv.org/help/api/user-manual.html
        #_entry_metadata
    [5] ArXiv identifier format: https://info.arxiv.org/help/arxiv_identifier.html
"""

import collections
import datetime
import enum
import re
from dataclasses import dataclass
from typing import List, Union
from urllib import parse
from xml.etree import ElementTree

from defusedxml import ElementTree as SecureElementTree
from requests_ratelimiter import LimiterSession

# Impose the public ratelimit by default [2]
SESSION = LimiterSession(per_minute=20)

# Define the base URL for the Arxiv API [1]
URL_BASE = "http://export.arxiv.org/api/"
URL_QUERY = URL_BASE + "query"

# Define XML tags for the Arxiv API [4]
TAG_PREFIX = "{http://www.w3.org/2005/Atom}"
TAG_ENTRY = "entry"
TAG_TITLE = "title"
TAG_ID = "id"
TAG_PUBLISHED = "published"
TAG_UPDATED = "updated"
TAG_SUMMARY = "summary"
TAG_AUTHOR = "author"
TAG_NAME = "name"
TAG_AFFILIATION = "affiliation"
TAG_CATEGORY = "category"
TAG_TERM = "term"
TAG_SCHEME = "scheme"

# Identifier schema (NEW)
ID_PREFIX = "http://arxiv.org/abs/"
ID_NUM_PATTERN_NEW = r"[0-9]{4}\.[0-9]{4,5}"
ID_VERSION_PATTERN_NEW = "[0-9]+"
# ID Pattern with named groups for the number and version
ID_PATTERN_NEW = (
    f"(?P<number>{ID_NUM_PATTERN_NEW})(?:v(?P<version" f">{ID_VERSION_PATTERN_NEW}))?"
)

# Identifier schema (OLD) example: math.GT/0309136
ID_NUM_PATTERN = "[a-z-]+/[0-9]{6,8}"
ID_PATTERN_OLD = f"(?P<number>{ID_NUM_PATTERN})"

# Define author fields
FIELD_AUTHOR_NAME = "name"
FIELD_AUTHOR_AFFILIATION = "affiliation"
FIELDS_AUTHOR = (
    FIELD_AUTHOR_NAME,
    FIELD_AUTHOR_AFFILIATION,
)

# Define category fields
FIELD_CATEGORY_TERM = "term"
FIELD_CATEGORY_SCHEME = "scheme"
FIELDS_CATEGORY = (
    FIELD_CATEGORY_TERM,
    FIELD_CATEGORY_SCHEME,
)

# Define entry fields
FIELD_ENTRY_TITLE = "title"
FIELD_ENTRY_ID = "id"
FIELD_ENTRY_PUBLISHED = "published"
FIELD_ENTRY_UPDATED = "updated"
FIELD_ENTRY_SUMMARY = "summary"
FIELD_ENTRY_AUTHOR = "author"
FIELD_ENTRY_CATEGORY = "category"
FIELDS_ENTRY = (
    FIELD_ENTRY_TITLE,
    FIELD_ENTRY_ID,
    FIELD_ENTRY_PUBLISHED,
    FIELD_ENTRY_UPDATED,
    FIELD_ENTRY_SUMMARY,
    FIELD_ENTRY_AUTHOR,
    FIELD_ENTRY_CATEGORY,
)


Category = collections.namedtuple("Category", " ".join(FIELDS_CATEGORY))


@dataclass
class Author:
    """A dataclass for an author of an Arxiv entry.

    Args:
        name:
            str, the name of the author.
        affiliation:
            str, the affiliation of the author.
    """

    name: str
    affiliation: str

    def __str__(self) -> str:
        """Return the author as a string."""
        return self.name


@dataclass
class Identifier:
    """A dataclass for an Arxiv identifier.

    Args:
        number:
            str, the number of the identifier.
        version:
            str, the version of the identifier.
        is_new:
            bool, whether the identifier is in the new format.
    """

    number: str
    version: str
    is_new: bool

    def __str__(self) -> str:
        """Return the identifier as a string."""
        if self.is_new:
            return f"{self.number}v{self.version}" if self.version else self.number
        return self.number

    def link(self) -> str:
        """Formatted arxiv link for the identifier"""
        return f"{ID_PREFIX}{self}"


def parse_identifier(id_text: str) -> Identifier:
    """Parse an Arxiv identifier into its components.

    Args:
        id_text:
            str, the Arxiv identifier to parse.
    """
    # Check if the identifier starts with the url prefix, if so remove
    if id_text.startswith(ID_PREFIX):
        id_text = id_text[len(ID_PREFIX) :]

    # Check if the identifier is in the new format
    match = re.match(ID_PATTERN_NEW, id_text)
    if match:
        return Identifier(
            number=match.group("number"),
            version=match.group("version"),
            is_new=True,
        )

    # Check if the identifier is in the old format
    match = re.match(ID_PATTERN_OLD, id_text)
    if match:
        return Identifier(
            number=match.group("number"),
            version=None,
            is_new=False,
        )

    # If the identifier does not match either pattern, raise an error
    raise ValueError(f"Invalid Arxiv identifier: {id_text}")


@dataclass
class Entry:
    """A dataclass for an entry from the Arxiv API [4]

    Args:
        title:
            str, the title of the entry
        id:
            str, the Arxiv ID of the entry
        published:
            datetime.datetime, the published date of the entry
        updated:
            datetime.datetime, the updated date of the entry
        summary:
            str, the summary of the entry
        author:
            List[Author], the authors of the entry
        category:
            List[Category], the categories of the entry
    """

    title: str
    id: Identifier
    published: datetime.datetime
    updated: datetime.datetime
    summary: str
    author: List[Author]
    category: List[Category]

    def link(self) -> str:
        """Formatted arxiv link for the entry"""
        return f"https://arxiv.org/abs/{self.id}"

    def to_dict(self) -> dict:
        """Return the entry as a dictionary."""
        return {
            FIELD_ENTRY_TITLE: self.title,
            FIELD_ENTRY_ID: self.id,
            FIELD_ENTRY_PUBLISHED: self.published,
            FIELD_ENTRY_UPDATED: self.updated,
            FIELD_ENTRY_SUMMARY: self.summary,
            FIELD_ENTRY_AUTHOR: self.author,
            FIELD_ENTRY_CATEGORY: self.category,
        }

    @staticmethod
    def from_dict(data: dict) -> "Entry":
        """Create an entry from a dictionary."""
        return Entry(
            title=data[FIELD_ENTRY_TITLE],
            id=data[FIELD_ENTRY_ID],
            published=data[FIELD_ENTRY_PUBLISHED],
            updated=data[FIELD_ENTRY_UPDATED],
            summary=data[FIELD_ENTRY_SUMMARY],
            author=data[FIELD_ENTRY_AUTHOR],
            category=data[FIELD_ENTRY_CATEGORY],
        )

    def filter_authors(self, authors: List[str]) -> bool:
        """Check if the entry has any of the given authors.

        Args:
            authors:
                List[str], the list of authors to check for.

        Returns:
            bool: True if the entry has any of the authors, False otherwise.
        """
        lower_authors = [author.lower().strip() for author in authors]
        return any(author.name.lower().strip() in lower_authors for author in self.author)


class SortBy(str, enum.Enum):
    """Enumeration of sort fields for the Arxiv API [3]"""

    Relevance = "relevance"
    LastUpdatedDate = "lastUpdatedDate"
    SubmittedDate = "submittedDate"


class SortOrder(str, enum.Enum):
    """Enumeration of sort orders for the Arxiv API [3]"""

    Ascending = "ascending"
    Descending = "descending"


class SearchField:
    """Enumeration of search fields for the Arxiv API [3]"""

    TITLE = "ti"
    AUTHOR = "au"
    ABSTRACT = "abs"
    COMMENT = "co"
    JOURNAL_REFERENCE = "jr"
    CATEGORY = "cat"
    REPORT_NUMBER = "rn"
    ID = "id"
    ALL = "all"


class LogicalOperator:
    """Enumeration of logical operators for the Arxiv API [3]"""

    AND = " AND "
    OR = " OR "
    AND_NOT = " ANDNOT "


def find(
    entry: ElementTree.Element, tag: str, find_all: bool = False
) -> Union[str, List[str]]:
    """Find the tag in the entry and return the text.

    Args:
        entry (ElementTree.Element): The entry to search.
        tag (str): The tag to search for.

    Returns:
        str: The text of the tag.
    """
    if not tag.startswith(TAG_PREFIX):
        tag = TAG_PREFIX + tag

    if find_all:
        return entry.findall(tag)

    res = entry.find(tag)
    if res is not None:
        return res.text


def parse_entry(entry: ElementTree.Element) -> Entry:
    """Parse an entry from the Arxiv API response.

    Args:
        entry (ElementTree.Element): The entry to parse.

    Returns:
        Entry: The parsed entry.
    """
    # Parse the authors
    authors = [
        Author(name=find(author, TAG_NAME), affiliation=find(author, TAG_AFFILIATION))
        for author in find(entry, TAG_AUTHOR, find_all=True)
    ]

    # Parse the categories
    categories = [
        Category(term=category.attrib[TAG_TERM], scheme=category.attrib[TAG_SCHEME])
        for category in find(entry, TAG_CATEGORY, find_all=True)
    ]

    # Parse date-type fields
    published = find(entry, TAG_PUBLISHED)
    updated = find(entry, TAG_UPDATED)
    if published is not None:
        published = datetime.datetime.fromisoformat(published)
    if updated is not None:
        updated = datetime.datetime.fromisoformat(updated)

    # Parse components of the identifier
    raw_id = find(entry, TAG_ID)
    id_ = parse_identifier(raw_id)

    # Return the parsed entry
    return Entry(
        title=find(entry, TAG_TITLE),
        id=id_,
        published=published,
        updated=updated,
        summary=find(entry, TAG_SUMMARY),
        author=authors,
        category=categories,
    )


def get_and_parse(url: str, params: dict) -> List[Entry]:
    """Get and parse the response from the Arxiv API, the payloads
    are encoded using the Atom 1 XML format.

    Args:
        url (str): The endpoint to query
        params (dict): The parameters to pass to the query

    Returns:
        dict: The parsed response
    """
    # Get the response
    response = SESSION.get(url, params=params)

    # Check for failures
    if not response.ok:
        response.raise_for_status()

    # Parse the response securely into ElementTree
    root = SecureElementTree.fromstring(response.text)

    # TODO finish parsing response into a list of named tuples if no errors,
    #  otherwise raise the error
    if len(root) == 1 and root[0].tag == "error":
        raise ValueError(f"No results found. Error: {root[0].text}")

    entries = [parse_entry(entry) for entry in find(root, TAG_ENTRY, find_all=True)]

    # Return the parsed response
    return entries


def _extend_query(
    query: str,
    field: SearchField,
    value: Union[str, List[str]],
    how: LogicalOperator = LogicalOperator.AND,
    how_list: LogicalOperator = LogicalOperator.OR,
) -> str:
    """Extend the query with the given field and value.

    Args:
        query:
            str, The current query string.
        field:
            SearchField, The field to search in.
        value:
            Union[str, List[str]], The value to search for.
        how:
            LogicalOperator, The logical operator to use when adding the field.
        how_list:
            LogicalOperator, The logical operator to use when adding a list of values.

    Returns:
        str: The extended query string.
    """
    # Check if query exists, if so then extend with cross-field logical operator
    if query:
        query += how

    # Check if value is scalar or list, then extend query
    if isinstance(value, str):
        query += f"{field}:{value}"
    elif isinstance(value, list):
        query += f"({field}:{how_list.join(value)})"

    return query


def format_search_query(
    title: Union[str, List[str]] = None,
    author: Union[str, List[str]] = None,
    abstract: Union[str, List[str]] = None,
    comment: Union[str, List[str]] = None,
    journal_reference: Union[str, List[str]] = None,
    category: Union[str, List[str]] = None,
    report_number: Union[str, List[str]] = None,
    id_list: List[str] = None,
    all_: Union[str, List[str]] = None,
    how: LogicalOperator = LogicalOperator.AND,
    how_list: LogicalOperator = LogicalOperator.OR,
) -> Union[str, None]:
    """Format the search query for the Arxiv API.

    Args:
        title:
            Union[str, List[str]], optional, The title to search for. Defaults to None.
        author:
            Union[str, List[str]], optional, The author to search for. Defaults to None.
        abstract:
            Union[str, List[str]], optional, The abstract to search for. Defaults to
            None.
        comment:
            Union[str, List[str]], optional, The comment to search for. Defaults to
            None.
        journal_reference:
            Union[str, List[str]], optional, The journal reference to search for.
            Defaults to None.
        category:
            Union[str, List[str]], optional, The category to search for. Defaults to
            None.
        report_number:
            Union[str, List[str]], optional, The report number to search for.
            Defaults to None.
        id_list:
            List[str], optional, The list of Arxiv IDs to search for. Defaults to None.
        all_:
            Union[str, List[str]], optional, The all field to search for. Defaults to
            None.
        how:
            LogicalOperator, optional, The logical operator to use when adding the
            field. Defaults to LogicalOperator.AND.
        how_list:
            LogicalOperator, optional, The logical operator to use when adding a list
            of values. Defaults to LogicalOperator.OR.

    Returns:
        str or None: The formatted query string, or None if no fields are provided.
    """
    # Short-circuit if no fields are provided
    if all(
        v is None
        for v in (
            title,
            author,
            abstract,
            comment,
            journal_reference,
            category,
            report_number,
            id_list,
            all_,
        )
    ):
        return None

    query = ""

    for field, value in zip(
        (
            SearchField.TITLE,
            SearchField.AUTHOR,
            SearchField.ABSTRACT,
            SearchField.COMMENT,
            SearchField.JOURNAL_REFERENCE,
            SearchField.CATEGORY,
            SearchField.REPORT_NUMBER,
            SearchField.ID,
            SearchField.ALL,
        ),
        (
            title,
            author,
            abstract,
            comment,
            journal_reference,
            category,
            report_number,
            id_list,
            all_,
        ),
    ):
        if value is not None:
            query = _extend_query(query, field, value, how=how, how_list=how_list)

    return parse.quote(query, safe="/:&=")


def execute(
    search_query: str = None,
    id_list: List[str] = None,
    start: int = 0,
    max_results: int = 10,
    sort_by: SortBy = SortBy.Relevance,
    sort_order: SortOrder = SortOrder.Descending,
    min_date: datetime.datetime = None,
    max_date: datetime.datetime = None,
    date_filter_field: str = FIELD_ENTRY_UPDATED,

) -> List[Entry]:
    """Query the Arxiv API with the given parameters.

    Args:
        search_query:
            str, optional, The query string to search for. Defaults to None.
        id_list:
            List[str], optional, A list of Arxiv IDs to search for. Defaults to None.
        start:
            int, optional, The index to start the search from. Defaults to 0.
        max_results:
            int, optional, The maximum number of results to return. Defaults to 10.
        sort_by:
            SortBy, optional, The field to sort by. Defaults to SortBy.Relevance.
        sort_order:
            SortOrder, optional, The order to sort by. Defaults to SortOrder.Descending.

    Returns:
        List[Entry]: The list of entries returned by the query.
    """
    # Define the parameters for the query
    params = {
        "search_query": search_query,
        "id_list": id_list,
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by.value,
        "sortOrder": sort_order.value,
    }

    # Filter out the None values
    params = {k: v for k, v in params.items() if v is not None}

    # Get and parse the response
    results = get_and_parse(URL_QUERY, params)

    # Filter for dates if specified
    if date_filter_field not in (FIELD_ENTRY_PUBLISHED, FIELD_ENTRY_UPDATED):
        raise ValueError(
            f"Invalid date filter field: {date_filter_field}, options "
            f"are {FIELD_ENTRY_PUBLISHED} or {FIELD_ENTRY_UPDATED}"
        )
    if min_date is not None:
        results = [r for r in results if getattr(r, date_filter_field) >= min_date]
    if max_date is not None:
        results = [r for r in results if getattr(r, date_filter_field) <= max_date]

    # Return the results
    return results


def query(
    title: Union[str, List[str]] = None,
    author: Union[str, List[str]] = None,
    abstract: Union[str, List[str]] = None,
    comment: Union[str, List[str]] = None,
    journal_reference: Union[str, List[str]] = None,
    category: Union[str, List[str]] = None,
    report_number: Union[str, List[str]] = None,
    id_list: List[str] = None,
    all_: Union[str, List[str]] = None,
    how: LogicalOperator = LogicalOperator.AND,
    how_list: LogicalOperator = LogicalOperator.OR,
    start: int = 0,
    max_results: int = 10,
    sort_by: SortBy = SortBy.Relevance,
    sort_order: SortOrder = SortOrder.Descending,
    min_date: datetime.datetime = None,
    max_date: datetime.datetime = None,
    date_filter_field: str = FIELD_ENTRY_UPDATED,
) -> List[Entry]:
    """Query the Arxiv API with the given parameters.

    Args:
        title:
            Union[str, List[str]], optional, The title to search for. Defaults to None.
        author:
            Union[str, List[str]], optional, The author to search for. Defaults to None.
        abstract:
            Union[str, List[str]], optional, The abstract to search for. Defaults to
            None.
        comment:
            Union[str, List[str]], optional, The comment to search for. Defaults to
            None.
        journal_reference:
            Union[str, List[str]], optional, The journal reference to search for.
            Defaults to None.
        category:
            Union[str, List[str]], optional, The category to search for. Defaults to
            None.
        report_number:
            Union[str, List[str]], optional, The report number to search for.
            Defaults to None.
        id_list:
            List[str], optional, The list of Arxiv IDs to search for. Defaults to None.
        all_:
            Union[str, List[str]], optional, The all field to search for. Defaults to
            None.
        how:
            LogicalOperator, optional, The logical operator to use when adding the
            field. Defaults to LogicalOperator.AND.
        how_list:
            LogicalOperator, optional, The logical operator to use when adding a list
            of values. Defaults to LogicalOperator.OR.
        start:
            int, optional, The index to start the search from. Defaults to 0.
        max_results:
            int, optional, The maximum number of results to return. Defaults to 10.
        sort_by:
            SortBy, optional, The field to sort by. Defaults to SortBy.Relevance.
        sort_order:
            SortOrder, optional, The order to sort by. Defaults to SortOrder.Descending.
    """
    # Format the search query
    search_query = format_search_query(
        title,
        author,
        abstract,
        comment,
        journal_reference,
        category,
        report_number,
        id_list,
        all_,
        how,
        how_list,
    )

    # Short-circuit if no search query is provided
    if search_query is None and id_list is None:
        raise ValueError("No search query provided; cannot query the entire Arxiv.")

    # Query the API
    return execute(
        search_query=search_query,
        id_list=id_list,
        start=start,
        max_results=max_results,
        sort_by=sort_by,
        sort_order=sort_order,
        min_date=min_date,
        max_date=max_date,
        date_filter_field=date_filter_field,
    )
