# -*- coding: utf-8 -*-

from enum import Enum, auto, unique


@unique
class ControlMode(Enum):
    normal = auto()
    node_moving = auto()
    pin_connecting = auto()
    roi_box = auto()
