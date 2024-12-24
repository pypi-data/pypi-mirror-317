"""
core.main

Core functionality and entry points for the package.
"""

import lxml
import numpy as np
import os
import pandas as pd
import requests
import sys

from pathlib import Path

from bs4 import BeautifulSoup
from typing import (
    Any, Dict, List, Literal, Optional, Protocol, Set, Tuple, TypeAlias
)

# Constants
SCOUNDREL_DIR = os.getenv("SCOUNDREL_DIR") if os.getenv("SCOUNDREL_DIR") is not None else Path("~/scoundrel").expanduser()
if not SCOUNDREL_DIR.exists():
    SCOUNDREL_DIR.mkdir(parents=True, exist_ok=True)


class Scoundrel:
    """
    Instantiation creates a Scoundrel object, which provides various
    web-scraping/-crawling tools.
    """
    def __init__(
        self,
        target: str,
        parser: Literal["lxml", "xml", "html.parser", "html5lib"] = "lxml"
    ) -> None:
        self.parser = parser
        self.target = target
        self.soup: BeautifulSoup | None = None

        self.html: str = self.get(self.target)


    def get(self, target) -> str:
        """
        Gets the content from `target`.
        """

        return requests.get(target).text


    def parse(self) -> bool:
        """
        Parses the content retured by `Scoundrel.get()`.
        """
        try:
            self.soup = BeautifulSoup(self.html, self.parser)
            self.html = self.soup.prettify()

            return 0
        except Exception as e:
            print(e)

            return 1
       

    def preserve(self) -> bool:
        """
        Saves the scraped and/or parsed web content to `SCOUNDREL_DIR`,
        which defaults to `~/scoundrel`. A different path can be specified
        by setting the `SCOUNDREL_DIR` environment variable prior to import.
        """
        try:
            title: str = self.soup.title.contents[0] or "untitled"
            with open(f"{SCOUNDREL_DIR}/{title}.txt", "w") as f:
                f.write(self.html)
            
            return 0
        except Exception as e:
            print(e)

            return 1


    def transgress(self):
        """
        Unimplemented.
        """
        pass


def main() -> None: return


if __name__ == "__main__":
    main()

