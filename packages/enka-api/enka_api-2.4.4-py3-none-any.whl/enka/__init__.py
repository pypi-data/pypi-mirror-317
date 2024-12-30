from __future__ import annotations

import warnings

from . import errors as errors
from . import gi as gi
from . import hsr as hsr
from . import utils as utils
from .clients import GenshinClient as GenshinClient
from .clients import HSRClient as HSRClient
from .clients import cache as cache
from .enums.enum import Game as Game
from .models.enka import *

warnings.warn(
    "The `enka-api` package has been renamed to `enka`, use `pip install enka` to install the new package.",
    DeprecationWarning,
    stacklevel=2,
)
