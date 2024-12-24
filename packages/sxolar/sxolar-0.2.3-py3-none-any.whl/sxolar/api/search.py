"""Higher-level api for searching for papers, uses an object interface
with overridden magic methods for syntactic sugar
"""

import datetime
from typing import Iterable, List, Union

from sxolar.api import arxiv
from sxolar.api.arxiv import (
    FIELD_ENTRY_UPDATED,
    LogicalOperator,
    SearchField,
    SortBy,
    SortOrder,
)


class Query:
    """Represents a query clause for the arxiv API

    Attributes:
        value (str): The value to search for
        operator (str): The operator to use
    """

    def __init__(
        self,
        value: str,
        filter_authors: List[str] = None,
    ):
        """Creates a new query

        Args:
            value:
                str, the value to search for
            filter_authors:
                List[str], the authors to filter by
        """
        self.value = value
        self.filter_authors = filter_authors or []

    def __str__(self):
        """Returns the string representation of the query"""
        return self.value

    def __and__(self, other):
        """Overloads the and operator to create a new query"""
        return self.and_(other)

    def __or__(self, other):
        """Overloads the or operator to create a new query"""
        return self.or_(other)

    def __sub__(self, other):
        """Overloads the subtraction operator to create a new query"""
        return self.and_not(other)

    def and_(self, other: Union[str, "Query"]):
        """Join two queries with the AND operator

        Args:
            other:
                str, the other query to join with

        Returns:
            Query: A new query object
        """
        return Query(
            f"{self}{LogicalOperator.AND}{other}",
            filter_authors=list(set(self.filter_authors) & set(other.filter_authors)),
        )

    def and_not(self, other):
        """Join two queries with the AND NOT operator

        Args:
            other:
                str, the other query to join with

        Returns:
            Query: A new query object
        """
        return Query(
            f"{self}{LogicalOperator.AND_NOT}{other}",
            filter_authors=list(set(self.filter_authors) - set(other.filter_authors)),
        )

    def or_(self, other):
        """Join two queries with the OR operator

        Args:
            other:
                str, the other query to join with

        Returns:
            Query: A new query object
        """
        return Query(
            f"{self}{LogicalOperator.OR}{other}",
            filter_authors=list(set(self.filter_authors) | set(other.filter_authors)),
        )

    def join(
        self, *others: Iterable["Query"], operator: LogicalOperator = LogicalOperator.OR
    ):
        """Join multiple queries with an operator

        Args:
            others:
                Iterable[Query], the queries to join
            operator:
                LogicalOperator, the operator to use to join the queries

        Returns:
            Query: A new query object
        """
        if not others:
            return self

        value = self.value
        authors = set(self.filter_authors)
        for other in others:
            value = f"{value}{operator}{other}"
            authors |= set(other.filter_authors)

        return Query(value, filter_authors=list(sorted(authors))).wrap()

    def wrap(self):
        """Wrap the query in parenthesis

        Returns:
            Query: A new query object
        """
        return Query(f"({self})", filter_authors=self.filter_authors)

    def search(
        self,
        start: int = 0,
        max_results: int = 10,
        sort_by: SortBy = SortBy.Relevance,
        sort_order: SortOrder = SortOrder.Descending,
        min_date: datetime.datetime = None,
        max_date: datetime.datetime = None,
        date_filter_field: str = FIELD_ENTRY_UPDATED,
    ):
        """Searches the arxiv API with the query

        Args:
            start:
                int, optional, The starting index of the results
            max_results:
                int, optional, The maximum number of results to return

        Returns:
            list: A list of dictionaries representing the search results
        """
        results = arxiv.execute(
            self.value,
            id_list=None,
            start=start,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order,
            min_date=min_date,
            max_date=max_date,
            date_filter_field=date_filter_field,
        )

        # Apply filter authors if any
        if self.filter_authors:
            results = [
                entry for entry in results if entry.filter_authors(self.filter_authors)
            ]

        return results

    def to_str(self) -> str:
        """Returns the string representation of the query"""
        return self.value

    @staticmethod
    def from_str(value: str):
        """Creates a new query from a string

        Args:
            value:
                str, the value to search for
        """
        return Query(value)

    @staticmethod
    def from_authors(*authors: Iterable[str]):
        """Creates a new author query

        Args:
            authors:
                str, the name of the author, "First Last"
        """
        authors = [Author(author).wrap() for author in authors]
        query = authors[0]
        if authors[1:]:
            query = query.join(*authors[1:], operator=LogicalOperator.OR)
        return query

    @staticmethod
    def from_titles(*titles: Iterable[str]):
        """Creates a new title query

        Args:
            titles:
                str, the title of the paper
        """
        titles = [Title(title) for title in titles]
        query = titles[0]
        if titles[1:]:
            query = query.join(*titles[1:], operator=LogicalOperator.OR)
        return query

    @staticmethod
    def from_abstracts(*abstracts: Iterable[str]):
        """Creates a new abstract query

        Args:
            abstracts:
                str, the abstract of the paper
        """
        abstracts = [Abstract(abstract) for abstract in abstracts]
        query = abstracts[0]
        if abstracts[1:]:
            query = query.join(*abstracts[1:], operator=LogicalOperator.OR)
        return query

    @staticmethod
    def from_alls(*alls: Iterable[str], operator: LogicalOperator = LogicalOperator.OR):
        """Creates a new all query

        Args:
            alls:
                str, the value to search for
        """
        alls = [All(all_) for all_ in alls]
        query = alls[0]
        if alls[1:]:
            query = query.join(*alls[1:], operator=operator)
        return query

    @staticmethod
    def from_journal_refs(*journal_refs: Iterable[str]):
        """Creates a new journal reference query

        Args:
            journal_refs:
                str, the journal reference
        """
        journal_refs = [JournalRef(journal_ref) for journal_ref in journal_refs]
        query = journal_refs[0]
        if journal_refs[1:]:
            query = query.join(*journal_refs[1:], operator=LogicalOperator.OR)
        return query

    @staticmethod
    def from_categories(*categories: Iterable[str]):
        """Creates a new category query

        Args:
            categories:
                str, the category
        """
        categories = [Category(category) for category in categories]
        query = categories[0]
        if categories[1:]:
            query = query.join(*categories[1:], operator=LogicalOperator.OR)
        return query

    @staticmethod
    def from_combo(
        authors: Iterable[str] = None,
        titles: Iterable[str] = None,
        abstracts: Iterable[str] = None,
        alls: Iterable[str] = None,
        journal_refs: Iterable[str] = None,
        categories: Iterable[str] = None,
        operator: LogicalOperator = LogicalOperator.AND,
        filter_authors: bool = False,
        alls_operator: LogicalOperator = LogicalOperator.OR,
    ):
        """Creates a new combo query

        Args:
            authors:
                Iterable[str], the name of the author, "First Last"
            titles:
                Iterable[str], the title of the paper
            abstracts:
                Iterable[str], the abstract of the paper
            alls:
                Iterable[str], the value to search for
            journal_refs:
                Iterable[str], the journal reference
            categories:
                Iterable[str], the category
        """
        queries = []
        if authors:
            queries.append(Query.from_authors(*authors))
        if titles:
            queries.append(Query.from_titles(*titles))
        if abstracts:
            queries.append(Query.from_abstracts(*abstracts))
        if alls:
            queries.append(Query.from_alls(*alls, operator=alls_operator))
        if journal_refs:
            queries.append(Query.from_journal_refs(*journal_refs))
        if categories:
            queries.append(Query.from_categories(*categories))

        query = queries[0]
        if queries[1:]:
            query = query.join(*queries[1:], operator=operator)

        # Add author filters if needed
        if filter_authors and authors:
            query.filter_authors = list(set(authors))

        return query


class Author(Query):
    """Represents an author query for the arxiv API"""

    def __init__(self, name: str):
        """Creates a new author query

        Args:
            name:
                str, the name of the author, "First Last"
        """
        if not name.startswith(SearchField.AUTHOR):
            name = f"{SearchField.AUTHOR}:{name}"
        super().__init__(name)


class Title(Query):
    """Represents a title query for the arxiv API"""

    def __init__(self, title: str):
        """Creates a new title query

        Args:
            title:
                str, the title of the paper
        """
        if not title.startswith(SearchField.TITLE):
            title = f"{SearchField.TITLE}:{title}"
        super().__init__(title)


class Abstract(Query):
    """Represents an abstract query for the arxiv API"""

    def __init__(self, abstract: str):
        """Creates a new abstract query

        Args:
            abstract:
                str, the abstract of the paper
        """
        if not abstract.startswith(SearchField.ABSTRACT):
            abstract = f"{SearchField.ABSTRACT}:{abstract}"
        super().__init__(abstract)


class All(Query):
    """Represents an all query for the arxiv API"""

    def __init__(self, all_: str):
        """Creates a new all query

        Args:
            all_:
                str, the value to search for
        """
        if not all_.startswith(SearchField.ALL):
            all_ = f"{SearchField.ALL}:{all_}"
        super().__init__(all_)


class JournalRef(Query):
    """Represents a journal reference query for the arxiv API"""

    def __init__(self, journal_ref: str):
        """Creates a new journal reference query

        Args:
            journal_ref:
                str, the journal reference
        """
        if not journal_ref.startswith(SearchField.JOURNAL_REFERENCE):
            journal_ref = f"{SearchField.JOURNAL_REFERENCE}:{journal_ref}"
        super().__init__(journal_ref)


class Category(Query):
    """Represents a category query for the arxiv API"""

    def __init__(self, category: str):
        """Creates a new category query

        Args:
            category:
        """
        if not category.startswith(SearchField.CATEGORY):
            category = f"{SearchField.CATEGORY}:{category}"
        super().__init__(category)
