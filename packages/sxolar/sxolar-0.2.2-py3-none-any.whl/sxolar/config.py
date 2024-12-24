"""Utilities for reading and writing configuration files for sxolar

Useful for storing user preferences and settings for saved queries
and configured summaries.

Sample Config file:

The example below defines 2 summaries, each with a list of sections.
Each section has a name, a list of authors, a list of topics, and a trailing
time period.

```yaml
summary name 1:
  - name: "Section 1: Topic A x Authors 1, 2 | Recent 2 Weeks"
    authors: ["Author 1", "Author 2"]
    alls: ["Topic A"]
    trailing:
      num: 14
      unit: "days"

  - name: "Section 2: Topic B x Authors 3, 4 | Recent 2 Months"
    authors: ["Author 3", "Author 4"]
    alls: ["Topic B"]
    trailing:
      num: 2
      unit: "months"

summary name 2:
  - name: "Section 1: Topic C x Authors 5, 6"
    authors: ["Author 5", "Author 6"]
    alls: ["Topic C"]
```

"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Union

from ruamel.yaml import YAML

from sxolar.summary import Section, Summary


@dataclass
class Config:
    """Configuration settings for sxolar

    Args:
        named_queries: A dictionary of named queries
    """

    info: dict
    summaries: Dict[str, Summary] = None

    def __post_init__(self):
        """Initialize the configuration settings"""
        # Parse the summaries from the configuration settings
        self.summaries = {}
        for name, sections in self.info.items():
            # Create the sections for the summary
            _sections = []
            for section in sections:
                _sec = Section.from_combo(**section)
                _sections.append(_sec)

            # Create the summary
            self.summaries[name] = Summary(name=name, sections=_sections)

    @staticmethod
    def load(path: Union[str, Path]):
        """Load a configuration file from a given path

        Args:
            path: str, the path to the configuration file

        Returns:
            Config, the configuration settings
        """
        yaml = YAML(typ="safe", pure=True)
        with open(path, "r") as f:
            data = yaml.load(f)
        return Config(info=data)
