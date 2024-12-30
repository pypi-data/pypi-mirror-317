# -*- coding: utf-8 -*-

from math import isqrt
from typing import Mapping, Tuple

import imgui

from cvp.config.sections.font import FontManagerConfig
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child
from cvp.imgui.clipboard import put_clipboard_text
from cvp.imgui.draw_list.get_draw_list import get_window_draw_list
from cvp.imgui.fonts.font import Font
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.push_item_width import item_width
from cvp.imgui.slider_float import slider_float
from cvp.imgui.text_centered import text_centered
from cvp.types.colors import RGBA
from cvp.types.override import override
from cvp.widgets.manager import Manager


class FontManager(Manager[FontManagerConfig, Font]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(
            context=context,
            window_config=context.config.font_manager,
            title="Font",
            closable=True,
            flags=None,
        )
        self._fonts = fonts

    @property
    def range_select_width(self) -> float:
        return self.window_config.range_select_width

    @range_select_width.setter
    def range_select_width(self, value: float) -> None:
        self.window_config.range_select_width = value

    @property
    def min_range_select_width(self) -> float:
        return self.window_config.min_range_select_width

    @property
    def max_range_select_width(self) -> float:
        return self.window_config.max_range_select_width

    @property
    def selected_block(self) -> Tuple[int, int]:
        return self.window_config.selected_block

    @selected_block.setter
    def selected_block(self, value: Tuple[int, int]) -> None:
        self.window_config.selected_block = value

    @property
    def selected_begin(self) -> int:
        return self.selected_block[0]

    @property
    def selected_end(self) -> int:
        return self.selected_block[1]

    @property
    def text_color(self) -> RGBA:
        return self.window_config.text_color

    @property
    def normal_stroke_color(self) -> RGBA:
        return self.window_config.normal_stroke_color

    @property
    def error_stroke_color(self) -> RGBA:
        return self.window_config.error_stroke_color

    @override
    def get_menus(self) -> Mapping[str, Font]:
        return {key: value for key, value in self._fonts.items()}

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_menu(self, key: str, item: Font) -> None:
        imgui.text("Font information")
        imgui.separator()

        input_text_disabled("Font family", item.family)
        input_text_disabled("Font pixel size", str(item.size))

        with begin_child("Planes", width=self.range_select_width):
            with item_width(-1):
                self.slider_range_select_width()
                list_box = imgui.begin_list_box("##Planes", width=-1, height=-1)
                if list_box.opened:
                    with list_box:
                        self.selectable_blocks(item)

        imgui.same_line()

        with begin_child("Codepoints", width=-1, height=-1, border=True):
            self.draw_codepoint_matrix(item)

    def slider_range_select_width(self) -> None:
        result = slider_float(
            "## Unicode Range List Width",
            self.range_select_width,
            self.min_range_select_width,
            self.max_range_select_width,
            "List width (%.3f)",
        )
        if result:
            self.range_select_width = result.value

    def selectable_blocks(self, item: Font) -> None:
        for block in item.blocks:
            begin, end = block
            label = f"{begin:06X}-{end:06X}"
            if imgui.selectable(label, block == self.selected_block)[1]:
                self.selected_block = block

    def draw_codepoint_matrix(self, item: Font) -> None:
        if self.selected_block not in item.blocks:
            text_centered("Please select a item")
            return

        codepoint_begin = self.selected_begin
        normal_stroke_color = imgui.get_color_u32_rgba(*self.normal_stroke_color)
        error_stroke_color = imgui.get_color_u32_rgba(*self.error_stroke_color)
        text_color = imgui.get_color_u32_rgba(*self.text_color)
        padding = self.window_config.padding
        rounding = self.window_config.rounding
        rect_flags = self.window_config.rect_flags
        thickness = self.window_config.thickness

        cx, cy = imgui.get_cursor_screen_pos()
        draw_list = get_window_draw_list()
        cell_size = item.size
        block_step = item.block_step
        line_count = isqrt(block_step)

        for i in range(block_step):
            x = i % line_count
            y = i // line_count

            x1 = cx + x * (cell_size + padding)
            y1 = cy + y * (cell_size + padding)
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            roi = x1, y1, x2, y2
            codepoint = codepoint_begin + i
            cp_detail = item.get_codepoint_info(codepoint)
            stroke_color = normal_stroke_color if cp_detail else error_stroke_color

            draw_list.add_rect(*roi, stroke_color, rounding, rect_flags, thickness)

            if cp_detail:
                with item:
                    draw_list.add_text(x1, y1, text_color, cp_detail.character)

            if self.focused and imgui.is_mouse_hovering_rect(*roi):
                if self.is_mouse_left_button_clicked():
                    put_clipboard_text(cp_detail.as_printable_unicode())
                    self.toast("Copied to clipboard")

                with imgui.begin_tooltip():
                    message = cp_detail.as_unformatted_text()
                    imgui.text_unformatted(message.strip())
