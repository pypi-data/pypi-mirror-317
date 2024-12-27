"""
Solid Operational Long-term Dynamics API

Examples
--------
from soldapi.core import qwork
duck1 = qwork.DuckLike(complex_object1)
duck2 = qwork.DuckLike(complex_object2)
print(duck1 - duck2)
print(duck2 - duck1)
"""

import logging

# from .core import qwork  # Chores like pathing, time utils.


# __all__ = ["qwork"]

logging.getLogger("soldapi").addHandler(logging.NullHandler())
