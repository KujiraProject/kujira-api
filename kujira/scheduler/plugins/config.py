# -*- coding: utf-8 -*-
"""Map plugin's names to types"""

from kujira.scheduler.plugins import osd
from kujira.scheduler.plugins import mon

PLUGINS = {
    "osd.add": osd.Add,
    "osd.remove": osd.Remove,
    "mon.add": mon.Add,
    "mon.remove": mon.Remove,
}
