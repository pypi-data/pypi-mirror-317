# -*- coding: utf-8 -*-

from enum import StrEnum, auto, unique

import imgui

from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.text_centered import text_centered
from cvp.process.process import Process
from cvp.types.override import override
from cvp.widgets.tab import TabItem


@unique
class StreamType(StrEnum):
    stdout = auto()
    stderr = auto()


class ProcessStreamTab(TabItem[Process]):
    def __init__(self, context: Context, stream: StreamType):
        super().__init__(context, str(stream))
        self._stream = stream
        self._auto_scroll = True

    @classmethod
    def from_stdout(cls, context: Context):
        return cls(context, StreamType.stdout)

    @classmethod
    def from_stderr(cls, context: Context):
        return cls(context, StreamType.stderr)

    @override
    def on_item(self, item: Process) -> None:
        match self._stream:
            case StreamType.stdout:
                buffer = item.stdout_buffer
            case StreamType.stderr:
                buffer = item.stderr_buffer
            case _:
                assert False, "Inaccessible section"

        if buffer is None:
            text_centered(f"The {self.label} buffer does not exist")
            return

        buffer.update_safe()

        self._auto_scroll = imgui.checkbox("Auto Scroll", self._auto_scroll)[1]

        with begin_child("## Logging", border=True):
            imgui.text_unformatted(buffer.getvalue())

            if self._auto_scroll:
                # if imgui.get_scroll_y() >= imgui.get_scroll_max_y()
                imgui.set_scroll_here_y(1.0)
