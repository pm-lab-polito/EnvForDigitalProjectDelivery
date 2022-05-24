"""
Module for utility functions
"""

import time


def current_milli_time():
    """
    Returns the current time in milliseconds

    :return:
    """
    return round(time.time() * 1000)
