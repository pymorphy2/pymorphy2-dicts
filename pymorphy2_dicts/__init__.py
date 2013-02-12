# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

def get_path():
    """
    Return path to dictionary.
    """
    return os.path.join(os.path.dirname(__file__), 'data')
