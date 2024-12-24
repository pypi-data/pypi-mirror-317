"""Tests for search api
"""

from sxolar.api.search import Author, Title, Query, Abstract, All, JournalRef, Category


class TestQuery:
    """Test the Query base class"""

    def test_create(self):
        """Test the creation of a query"""
        q = Query('au:del maestro')
        assert isinstance(q, Query)
        assert q.value == 'au:del maestro'

    def test_str(self):
        """Test the string representation"""
        q = Query('au:del maestro')
        assert str(q) == 'au:del maestro'

    def test_and(self):
        """Test the and operator"""
        q = Query('au:del maestro')
        q2 = Query('ti:checkerboard')
        q3 = q & q2
        assert str(q3) == 'au:del maestro AND ti:checkerboard'

    def test_or(self):
        """Test the or operator"""
        q = Query('au:del maestro')
        q2 = Query('ti:checkerboard')
        q3 = q | q2
        assert str(q3) == 'au:del maestro OR ti:checkerboard'

    def test_and_not(self):
        """Test the and_not operator"""
        q = Query('au:del maestro')
        q2 = Query('ti:checkerboard')
        q3 = q - q2
        assert str(q3) == 'au:del maestro ANDNOT ti:checkerboard'

    def test_wrap(self):
        """Test the wrap function"""
        q = Query('au:del maestro')
        q2 = Query('ti:checkerboard')
        q3 = q & q2
        q4 = q3.wrap()
        assert str(q4) == '(au:del maestro AND ti:checkerboard)'

    def test_search(self):
        """Test the query function"""
        res = Author('del maestro').search()
        assert len(res) == 10

    def test_join(self):
        """Test the join function"""
        res = Author('del maestro').join(Title('checkerboard'))
        assert str(res) == '(au:del maestro OR ti:checkerboard)'


class TestSearchFieldClasses:
    """Test the search field classes"""

    def test_author(self):
        """Test the author class"""
        q = Author('del maestro')
        assert isinstance(q, Author)
        assert q.value == 'au:del maestro'

    def test_title(self):
        """Test the title class"""
        q = Title('checkerboard')
        assert isinstance(q, Title)
        assert q.value == 'ti:checkerboard'

    def test_abstract(self):
        """Test the abstract class"""
        q = Abstract('checkerboard')
        assert isinstance(q, Abstract)
        assert q.value == 'abs:checkerboard'

    def test_all(self):
        """Test the all class"""
        q = All('checkerboard')
        assert isinstance(q, All)
        assert q.value == 'all:checkerboard'

    def test_journal_ref(self):
        """Test the journal_ref class"""
        q = JournalRef('checkerboard')
        assert isinstance(q, JournalRef)
        assert q.value == 'jr:checkerboard'

    def test_category(self):
        """Test the category class"""
        q = Category('checkerboard')
        assert isinstance(q, Category)
        assert q.value == 'cat:checkerboard'
