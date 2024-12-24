"""Tests for config utilities
"""

import pathlib

from sxolar.config import Config

PATH_TESTS = pathlib.Path(__file__).parent


class TestConfig:
    """Test group for config utilities"""

    def test_load(self):
        """Test loading a configuration file"""
        # Given a path to a configuration file
        path = PATH_TESTS / "data" / "sample.yml"

        # When loading the configuration file
        config = Config.load(path)

        # Then the configuration settings should be loaded
        assert config.info == {
            "summary name 1": [
                {
                    "name": "Section 1: Topic A x Authors 1, 2 | Recent 2 Weeks",
                    "authors": ["Author 1", "Author 2"],
                    "alls": ["Topic A"],
                    "trailing": {"num": 14, "unit": "days"},
                },
                {
                    "name": "Section 2: Topic B x Authors 3, 4 | Recent 2 Months",
                    "authors": ["Author 3", "Author 4"],
                    "alls": ["Topic B"],
                    "trailing": {"num": 2, "unit": "months"},
                },
            ],
            "summary name 2": [
                {
                    "name": "Section 1: Topic C x Authors 5, 6",
                    "authors": ["Author 5", "Author 6"],
                    "alls": ["Topic C"],
                },
            ],
        }

    def test_summaries(self):
        """Test loading a configuration file"""
        # Given a path to a configuration file
        path = PATH_TESTS / "data" / "sample.yml"

        # When loading the configuration file
        config = Config.load(path)

        assert len(config.summaries) == 2
        assert list(sorted(config.summaries.keys())) == [
            "summary name 1",
            "summary name 2",
        ]

        # Check details of summary objects
        summary = config.summaries["summary name 1"]
        assert summary.name == "summary name 1"
        assert len(summary.sections) == 2
        assert (
            summary.sections[0].name
            == "Section 1: Topic A x Authors 1, 2 | Recent 2 Weeks"
        )
        assert str(summary.sections[0].query) == (
            "(((au:Author 1) OR (au:Author 2)) AND all:Topic A)"
        )
