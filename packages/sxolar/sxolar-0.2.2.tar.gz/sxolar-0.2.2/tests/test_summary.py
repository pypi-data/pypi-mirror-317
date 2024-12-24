"""Tests for the summary module
"""

import datetime

import pytest

from sxolar.api.arxiv import Author, Category, Entry, Identifier
from sxolar.summary import Format, Section, Summary


class TestSection:
    """Test the summary module"""

    @pytest.fixture(autouse=True, scope="class")
    def results(self):
        """Return a list of results"""
        return [
            Entry.from_dict(
                {
                    "author": [
                        Author(name="Adrian Del Maestro", affiliation=None),
                        Author(name="Ian Affleck", affiliation=None),
                    ],
                    "category": [
                        Category(
                            term="cond-mat.stat-mech",
                            scheme="http://arxiv.org/schemas/atom",
                        )
                    ],
                    "id": Identifier(number="1005.5383", version="1", is_new=True),
                    "published": datetime.datetime(
                        2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
                    ),
                    "summary": "  Harmonically trapped ultra-cold atoms and helium-4 in nanopores provide new\nexperimental realizations of bosons in one dim...eement is obtained after\nincluding the leading irrelevant interactions in the Hamiltonian which are\ndetermined explicitly.\n",
                    "title": "Interacting bosons in one dimension and Luttinger liquid theory",
                    "updated": datetime.datetime(
                        2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
                    ),
                }
            ),
            Entry.from_dict(
                {
                    "author": [
                        Author(name="C. M. Herdman", affiliation=None),
                        Author(name="A. Rommal", affiliation=None),
                        Author(name="A. Del Maestro", affiliation=None),
                    ],
                    "category": [
                        Category(
                            term="cond-mat.stat-mech",
                            scheme="http://arxiv.org/schemas/atom",
                        ),
                        Category(
                            term="cond-mat.other",
                            scheme="http://arxiv.org/schemas/atom",
                        ),
                    ],
                    "id": Identifier(number="1312.6177", version="1", is_new=True),
                    "published": datetime.datetime(
                        2013, 12, 20, 23, 48, 25, tzinfo=datetime.timezone.utc
                    ),
                    "summary": "  A path integral Monte Carlo method based on the worm algorithm has been\ndeveloped to compute the chemical potential of int...re. We speculate on future applications of the proposed\ntechnique, including its use in studies of confined quantum fluids.\n",
                    "title": "Quantum Monte Carlo measurement of the chemical potential of helium-4",
                    "updated": datetime.datetime(
                        2013, 12, 20, 23, 48, 25, tzinfo=datetime.timezone.utc
                    ),
                }
            ),
        ]

    def test_init(self):
        """Test the summary class"""
        smy = Section("Test", None, [])
        assert isinstance(smy, Section)
        assert smy.name == "Test"
        assert smy.results == []
        assert smy.max_authors == 3
        assert smy.include_abstract is False

    def test_format_entry_plain(self, results):
        """Test the format_entry method"""
        smy = Section("TestPlain", query=None, results=results)
        entry = smy.results[0]
        entry_str = smy._format_entry(entry, Format.Plain)
        assert isinstance(entry_str, str)
        assert entry_str == (
            "Interacting bosons in one dimension and Luttinger liquid theory "
            "[1005.5383v1]\n"
            "Adrian Del Maestro, Ian Affleck\n"
            "\n"
            "http://arxiv.org/abs/1005.5383v1\n"
        )

    def test_format_entry_html(self, results):
        """Test the format_entry method"""
        smy = Section("TestPlain", query=None, results=results)
        entry = smy.results[0]
        entry_str = smy._format_entry(entry, Format.Html)
        assert isinstance(entry_str, str)
        assert entry_str == (
            '<p><h3><a href="http://arxiv.org/abs/1005.5383v1">Interacting bosons in one '
            "dimension and Luttinger liquid theory [1005.5383v1]</a></h3><br>Adrian Del "
            "Maestro, Ian Affleck<br><br></p>"
        )

    def test_to_text(self, results):
        """Test the to_text method"""
        smy = Section("TestPlain", query=None, results=results)
        text = smy.to_text()
        assert isinstance(text, str)
        assert text == (
            "TestPlain:\n"
            "Interacting bosons in one dimension and Luttinger liquid theory "
            "[1005.5383v1]\n"
            "Adrian Del Maestro, Ian Affleck\n"
            "\n"
            "http://arxiv.org/abs/1005.5383v1\n"
            "\n"
            "Quantum Monte Carlo measurement of the chemical potential of helium-4 "
            "[1312.6177v1]\n"
            "C. M. Herdman, A. Rommal, A. Del Maestro\n"
            "\n"
            "http://arxiv.org/abs/1312.6177v1\n"
        )

    def test_to_html(self, results):
        """Test the to_html method"""
        smy = Section("TestHtml", query=None, results=results)
        html = smy.to_html()
        assert isinstance(html, str)
        assert html == (
            "<h2>TestHtml</h2>\n"
            '<p><h3><a href="http://arxiv.org/abs/1005.5383v1">Interacting bosons in one '
            "dimension and Luttinger liquid theory [1005.5383v1]</a></h3><br>Adrian Del "
            "Maestro, Ian Affleck<br><br></p>\n"
            '<p><h3><a href="http://arxiv.org/abs/1312.6177v1">Quantum Monte Carlo '
            "measurement of the chemical potential of helium-4 "
            "[1312.6177v1]</a></h3><br>C. M. Herdman, A. Rommal, A. Del "
            "Maestro<br><br></p>"
        )

    def test_refresh(self):
        """Test the refresh method"""
        smy = Section.from_combo("Test1", authors=["Adrian Del Maestro"])
        smy.refresh()
        assert smy.results is not None
        assert len(smy.results) == 50
        assert isinstance(smy.results[0], Entry)
        assert smy.results[0].author == [
            Author(name="Adrian Del Maestro", affiliation=None),
            Author(name="Ian Affleck", affiliation=None),
        ]
        assert smy.results[0].category == [
            Category(
                term="cond-mat.stat-mech",
                scheme="http://arxiv.org/schemas/atom",
            )
        ]
        assert smy.results[0].id == Identifier(
            number="1005.5383", version="1", is_new=True
        )
        assert smy.results[0].published == datetime.datetime(
            2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
        )
        assert smy.results[0].summary == (
            "  Harmonically trapped ultra-cold atoms and helium-4 in nanopores provide "
            "new\n"
            "experimental realizations of bosons in one dimension, motivating the search "
            "for\n"
            "a more complete theoretical understanding of their low energy properties. "
            "Worm\n"
            "algorithm path integral quantum Monte Carlo results for interacting bosons\n"
            "restricted to the one dimensional continuum are compared to the finite\n"
            "temperature and system size predictions of Luttinger liquid theory. For "
            "large\n"
            "system sizes at low temperature, excellent agreement is obtained after\n"
            "including the leading irrelevant interactions in the Hamiltonian which are\n"
            "determined explicitly.\n"
        )
        assert (
            smy.results[0].title
            == "Interacting bosons in one dimension and Luttinger liquid theory"
        )
        assert smy.results[0].updated == datetime.datetime(
            2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
        )


class TestSummary:
    """Test the summary module"""

    @pytest.fixture(autouse=True, scope="class")
    def results(self):
        """Return a list of results"""
        return [
            Entry.from_dict(
                {
                    "author": [
                        Author(name="Adrian Del Maestro", affiliation=None),
                        Author(name="Ian Affleck", affiliation=None),
                    ],
                    "category": [
                        Category(
                            term="cond-mat.stat-mech",
                            scheme="http://arxiv.org/schemas/atom",
                        )
                    ],
                    "id": Identifier(number="1005.5383", version="1", is_new=True),
                    "published": datetime.datetime(
                        2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
                    ),
                    "summary": "  Harmonically trapped ultra-cold atoms and helium-4 in nanopores provide new\nexperimental realizations of bosons in one dim...eement is obtained after\nincluding the leading irrelevant interactions in the Hamiltonian which are\ndetermined explicitly.\n",
                    "title": "Interacting bosons in one dimension and Luttinger liquid theory",
                    "updated": datetime.datetime(
                        2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
                    ),
                }
            ),
            Entry.from_dict(
                {
                    "author": [
                        Author(name="C. M. Herdman", affiliation=None),
                        Author(name="A. Rommal", affiliation=None),
                        Author(name="A. Del Maestro", affiliation=None),
                    ],
                    "category": [
                        Category(
                            term="cond-mat.stat-mech",
                            scheme="http://arxiv.org/schemas/atom",
                        ),
                        Category(
                            term="cond-mat.other",
                            scheme="http://arxiv.org/schemas/atom",
                        ),
                    ],
                    "id": Identifier(number="1312.6177", version="1", is_new=True),
                    "published": datetime.datetime(
                        2013, 12, 20, 23, 48, 25, tzinfo=datetime.timezone.utc
                    ),
                    "summary": "  A path integral Monte Carlo method based on the worm algorithm has been\ndeveloped to compute the chemical potential of int...re. We speculate on future applications of the proposed\ntechnique, including its use in studies of confined quantum fluids.\n",
                    "title": "Quantum Monte Carlo measurement of the chemical potential of helium-4",
                    "updated": datetime.datetime(
                        2013, 12, 20, 23, 48, 25, tzinfo=datetime.timezone.utc
                    ),
                }
            ),
        ]

    def test_to_text(self, results):
        """Test the to_text method"""
        sec1 = Section("TestSec1", query=None, results=results[:1])
        sec2 = Section("TestSec2", query=None, results=results[1:])
        smy = Summary("Test", [sec1, sec2])
        text = smy.to_text()
        assert isinstance(text, str)
        assert text == (
            "TestSec1:\n"
            "Interacting bosons in one dimension and Luttinger liquid theory "
            "[1005.5383v1]\n"
            "Adrian Del Maestro, Ian Affleck\n"
            "\n"
            "http://arxiv.org/abs/1005.5383v1\n"
            "\n"
            "\n"
            "TestSec2:\n"
            "Quantum Monte Carlo measurement of the chemical potential of helium-4 "
            "[1312.6177v1]\n"
            "C. M. Herdman, A. Rommal, A. Del Maestro\n"
            "\n"
            "http://arxiv.org/abs/1312.6177v1\n"
        )

    def test_to_html(self, results):
        """Test the to_text method"""
        sec1 = Section("TestSec1", query=None, results=results[:1])
        sec2 = Section("TestSec2", query=None, results=results[1:])
        smy = Summary("Test", [sec1, sec2])
        text = smy.to_html()
        assert isinstance(text, str)
        assert text == (
            "<h2>TestSec1</h2>\n"
            '<p><h3><a href="http://arxiv.org/abs/1005.5383v1">Interacting bosons in one '
            "dimension and Luttinger liquid theory [1005.5383v1]</a></h3><br>Adrian Del "
            "Maestro, Ian Affleck<br><br></p><br><br><h2>TestSec2</h2>\n"
            '<p><h3><a href="http://arxiv.org/abs/1312.6177v1">Quantum Monte Carlo '
            "measurement of the chemical potential of helium-4 "
            "[1312.6177v1]</a></h3><br>C. M. Herdman, A. Rommal, A. Del "
            "Maestro<br><br></p>"
        )

    def test_refresh(self):
        """Test the refresh method"""
        sec = Section.from_combo("Test1", authors=["Adrian Del Maestro"])
        smy = Summary("Test", [sec])
        smy.refresh()
        smy = smy.sections[0]
        assert smy.results is not None
        assert len(smy.results) == 50
        assert isinstance(smy.results[0], Entry)
        assert smy.results[0].author == [
            Author(name="Adrian Del Maestro", affiliation=None),
            Author(name="Ian Affleck", affiliation=None),
        ]
        assert smy.results[0].category == [
            Category(
                term="cond-mat.stat-mech",
                scheme="http://arxiv.org/schemas/atom",
            )
        ]
        assert smy.results[0].id == Identifier(
            number="1005.5383", version="1", is_new=True
        )
        assert smy.results[0].published == datetime.datetime(
            2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
        )
        assert smy.results[0].summary == (
            "  Harmonically trapped ultra-cold atoms and helium-4 in nanopores provide "
            "new\n"
            "experimental realizations of bosons in one dimension, motivating the search "
            "for\n"
            "a more complete theoretical understanding of their low energy properties. "
            "Worm\n"
            "algorithm path integral quantum Monte Carlo results for interacting bosons\n"
            "restricted to the one dimensional continuum are compared to the finite\n"
            "temperature and system size predictions of Luttinger liquid theory. For "
            "large\n"
            "system sizes at low temperature, excellent agreement is obtained after\n"
            "including the leading irrelevant interactions in the Hamiltonian which are\n"
            "determined explicitly.\n"
        )
        assert (
            smy.results[0].title
            == "Interacting bosons in one dimension and Luttinger liquid theory"
        )
        assert smy.results[0].updated == datetime.datetime(
            2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
        )
