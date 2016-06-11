# -*- coding: utf-8 -*-
"""Map plugin's names to types"""

from kujira.scheduler.plugins.osd.add import Add
from kujira.scheduler.plugins.osd.remove import Remove

PLUGINS = {
    "osd.add": Add,
    "osd.remove": Remove
}
