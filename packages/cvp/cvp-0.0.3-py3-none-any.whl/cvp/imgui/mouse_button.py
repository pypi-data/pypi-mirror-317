# -*- coding: utf-8 -*-

from enum import Enum, auto, unique
from typing import Optional

from cvp.patterns.delta import Delta
from cvp.types.shapes import Point


@unique
class ButtonState(Enum):
    normal = auto()
    ready = auto()
    dragging = auto()


class MouseButton:
    _pivot: Optional[Point]

    def __init__(self) -> None:
        self._down = Delta.from_single_value(False)
        self._drag = Delta.from_single_value(False)
        self._state = ButtonState.normal
        self._pivot = None

    @property
    def down(self):
        return self._down

    @property
    def drag(self):
        return self._drag

    @property
    def state(self):
        return self._state

    @property
    def pivot(self):
        return self._pivot

    @property
    def is_down(self) -> bool:
        return self._down.value

    @property
    def is_up(self) -> bool:
        return not self._down.value

    @property
    def changed_down(self) -> bool:
        return self._down.changed and self._down.value

    @property
    def changed_up(self) -> bool:
        return self._down.changed and not self._down.value

    @property
    def is_drag(self) -> bool:
        return self._drag.value

    @property
    def start_drag(self) -> bool:
        return self._drag.changed and self._drag.value

    @property
    def end_drag(self) -> bool:
        return self._drag.changed and not self._drag.value

    def update(self, down: bool, mouse_point: Point) -> None:
        if self._down.update(down):
            if self._down.value:
                self._state = ButtonState.ready
                self._pivot = mouse_point
            else:
                self._state = ButtonState.normal
                self._pivot = None

        if not self._down.value:
            assert self._state == ButtonState.normal
            assert self._pivot is None
            self._drag.update(False)
            return

        assert self._state != ButtonState.normal
        assert self._pivot is not None

        if self._state == ButtonState.ready and self._pivot != mouse_point:
            self._state = ButtonState.dragging

        self._drag.update(self._state == ButtonState.dragging)
