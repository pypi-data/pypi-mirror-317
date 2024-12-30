# -*- coding: utf-8 -*-

from typing import Final, Optional

from overrides import override
from yaml import Dumper


class IndentListDumper(Dumper):
    @override
    def increase_indent(self, flow=False, indentless=False):
        # Indent array elements.
        return super().increase_indent(flow, False)


class DefaultDumper(Dumper):
    _ROOT_INDENT: Final[int] = 0

    @override
    def increase_indent(self, flow=False, indentless=False):
        # Indent array elements.
        return super().increase_indent(flow, False)

    @override
    def write_line_break(self, data: Optional[str] = None) -> None:
        # Separate objects at root depth with newlines.
        super().write_line_break(data)
        if self.indent == self._ROOT_INDENT:
            super().write_line_break(data)
