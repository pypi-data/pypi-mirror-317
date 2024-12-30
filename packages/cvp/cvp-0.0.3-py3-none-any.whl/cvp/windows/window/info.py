# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class WindowInfoTab(TabItem[WindowBase]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: WindowBase) -> None:
        imgui.text("Key:")
        input_text_disabled("## Key", item.key)

        imgui.text("Title:")
        input_text_disabled("## Title", item.title)

        imgui.text("Label:")
        input_text_disabled("## Label", item.label)

        imgui.separator()
        imgui.text("Visibility:")

        if button("Show", disabled=item.opened):
            item.opened = True
        imgui.same_line()
        if button("Hide", disabled=not item.opened):
            item.opened = False

        imgui.separator()
        imgui.text("Geometry:")

        x, y = item.query.position
        w, h = item.query.size

        pos_result = imgui.drag_float2("Position", x, y)
        if pos_result[0]:
            pos_value = pos_result[1]
            x = pos_value[0]
            y = pos_value[1]
            imgui.set_window_position_labeled(item.label, x, y, imgui.ALWAYS)

        size_result = imgui.drag_float2("Size", w, h)
        if size_result[0]:
            size_value = size_result[1]
            w = size_value[0]
            h = size_value[1]
            imgui.set_window_size_named(item.label, w, h, imgui.ALWAYS)

        imgui.separator()
        imgui.text("Fullscreen:")
        if imgui.button("Work Area"):
            viewport = imgui.get_main_viewport()
            wx, wy = viewport.work_pos
            ww, wh = viewport.work_size
            imgui.set_window_position_labeled(item.label, wx, wy, imgui.ALWAYS)
            imgui.set_window_size_named(item.label, ww, wh, imgui.ALWAYS)
        imgui.same_line()
        if imgui.button("Main Area"):
            viewport = imgui.get_main_viewport()
            mx, my = viewport.pos
            mw, mh = viewport.size
            imgui.set_window_position_labeled(item.label, mx, my, imgui.ALWAYS)
            imgui.set_window_size_named(item.label, mw, mh, imgui.ALWAYS)

        imgui.separator()
        imgui.text("Options:")

        with imgui.begin_table("## OptionsTable", 3):
            imgui.table_next_column()
            if cb_result := checkbox("No titlebar", item.no_titlebar):
                item.no_titlebar = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No scrollbar", item.no_scrollbar):
                item.no_scrollbar = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No menu", item.no_menu):
                item.no_menu = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No move", item.no_move):
                item.no_move = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No resize", item.no_resize):
                item.no_resize = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No collapse", item.no_collapse):
                item.no_collapse = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("Closable", item.closable):
                item.closable = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No nav", item.no_nav):
                item.no_nav = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No background", item.no_background):
                item.no_background = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("No bring to front", item.no_bring_to_front):
                item.no_bring_to_front = cb_result.state

            imgui.table_next_column()
            if cb_result := checkbox("Unsaved document", item.unsaved_document):
                item.unsaved_document = cb_result.state
