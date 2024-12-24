# -----------------------------------------------------------------------------
#                               intersect_point.py
# =============================================================================
#  This is a part of geo - A Python package for practical geometry algorithms.
#
#  Last updated: 24 Dec 2024. Copyright (c) 2024 Minh-Chien Trinh
# -----------------------------------------------------------------------------

import numpy as np
from .check_intersect import check_intersect


def intersect_point(line1, line2):
    """Find the intersection point of two lines.
    Parameters:
        line1: an array of coords of 02 points
        line2: an array of coords of 02 points
    Returns:
        point: an array of coords of the intersection point
    """

    if check_intersect(line1, line2):
        
        point = np.array(3)

    return point