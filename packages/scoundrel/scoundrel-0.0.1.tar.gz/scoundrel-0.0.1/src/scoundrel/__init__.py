# scoundrel/__init__.py

import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup

from . import models
from . import protocols
from . import types
from .core import *


__all__ = [
    # Third-party exports
    "numpy",
    "np", # Alias for `numpy`
    "pandas",
    "pd", # Alias for `pandas`
    "requests",
    
    # Class/method exports
    "main",
    "Scoundrel"
]
