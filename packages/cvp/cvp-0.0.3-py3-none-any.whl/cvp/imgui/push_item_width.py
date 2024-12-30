# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Union

import imgui


@contextmanager
def item_width(width: Union[int, float]):
    imgui.push_item_width(width)
    try:
        yield
    finally:
        imgui.pop_item_width()


@contextmanager
def align_right_side():
    imgui.push_item_width(-imgui.FLOAT_MIN)
    try:
        yield
    finally:
        imgui.pop_item_width()
