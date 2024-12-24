"""Tests for the arxiv module.
"""

import datetime

from sxolar.api import arxiv


class TestArxivAPI:
    """Test the arxiv API"""

    def test_query(self):
        """Test the query function,

        This test mimicks the behavior of the API documentation, which gives "3" results
            Docs Test Query: "http://export.arxiv.org/api/query?search_query=au:del_maestro+ANDNOT+%28ti:checkerboard+OR+ti:Pyrochlore%29"
        """
        res = arxiv.query(author="del maestro")
        assert len(res) == 10

    def test_query_last_updated(self):
        """Test the query function,

        This test mimicks the behavior of the API documentation, which gives "3" results
            Docs Test Query: "http://export.arxiv.org/api/query?search_query=au:del_maestro+ANDNOT+%28ti:checkerboard+OR+ti:Pyrochlore%29"
        """
        # Make date filters for testing UTC
        date_end = datetime.datetime.now(datetime.UTC)
        date_start = date_end - datetime.timedelta(days=7)

        # Test the query
        res = arxiv.query(
            author="del maestro",
            sort_by=arxiv.SortBy.LastUpdatedDate,
            sort_order=arxiv.SortOrder.Descending,
            min_date=date_start,
            max_date=date_end,
        )

        # Check there is at least one result
        assert len(res) > 0

        # Check date filter worked
        for entry in res:
            assert date_start <= entry.updated <= date_end
