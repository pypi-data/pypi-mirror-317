# -*- coding: utf-8 -*-

import os
from os import PathLike
from pathlib import Path
from typing import Callable, List, Optional, Union

import imgui
import pygame

from cvp.imgui.begin_child import begin_child
from cvp.imgui.button import button
from cvp.imgui.footer_height_to_reserve import footer_height_to_reserve
from cvp.imgui.set_window_min_size import set_window_min_size
from cvp.logging.logging import logger
from cvp.renderer.popup.base import PopupBase
from cvp.types.override import override
from cvp.variables import MIN_POPUP_OPEN_FILE_HEIGHT, MIN_POPUP_OPEN_FILE_WIDTH

ENTER_RETURN = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
DOUBLE_CLICK = imgui.SELECTABLE_ALLOW_DOUBLE_CLICK


class OpenFilePopup(PopupBase[str]):
    _items: List[str]

    def __init__(
        self,
        title: Optional[str] = None,
        directory: Optional[Union[str, PathLike]] = None,
        show_hidden=False,
        centered=True,
        flags=0,
        *,
        min_width=MIN_POPUP_OPEN_FILE_WIDTH,
        min_height=MIN_POPUP_OPEN_FILE_HEIGHT,
        target: Optional[Callable[[str], None]] = None,
        oneshot: Optional[bool] = None,
    ):
        super().__init__(
            title,
            centered,
            flags,
            min_width=min_width,
            min_height=min_height,
            target=target,
            oneshot=oneshot,
        )

        if isinstance(directory, Path) and directory.is_dir():
            dir_path = directory
        elif isinstance(directory, str) and os.path.isdir(directory):
            dir_path = Path(directory)
        else:
            dir_path = Path.home()

        self._location_text = str(dir_path)
        self._current_dir = str()
        self._items = list()
        self._selected = str()

        self._parent_button_label = "Parent"
        self._location_input_label = "Location"
        self._hidden_checkbox_label = "Show Hidden"
        self._open_button_label = "Open"
        self._close_button_label = "Close"
        self._show_hidden = show_hidden

    @staticmethod
    def list_items(location: Union[str, PathLike], show_hidden=False) -> List[str]:
        dirs = list()
        files = list()

        items = os.listdir(location)
        items.sort()

        for item in items:
            if not show_hidden and item.startswith("."):
                continue
            item_path = os.path.join(location, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            elif os.path.isfile(item_path):
                files.append(item)

        return dirs + files

    @override
    def on_process(self) -> Optional[str]:
        if imgui.is_window_appearing():
            set_window_min_size(self._min_width, self._min_height)

        if imgui.button(self._parent_button_label):
            self._location_text = str(Path(self._location_text).parent)

        imgui.same_line()

        if imgui.checkbox(self._hidden_checkbox_label, self._show_hidden)[0]:
            self._show_hidden = not self._show_hidden
            self._items = self.list_items(self._current_dir, self._show_hidden)

        imgui.same_line()

        loc_text = self._location_text
        loc_changed, loc_text = imgui.input_text(
            self._location_input_label, loc_text, -1, ENTER_RETURN
        )

        if loc_changed:
            if os.path.isfile(loc_text):
                imgui.close_current_popup()
                return loc_text
            elif os.path.isdir(loc_text):
                self._location_text = loc_text
            else:
                logger.warning(f"Invalid location: '{loc_text}'")

        with begin_child("Files", 0, -footer_height_to_reserve(), border=True):
            if self._current_dir != self._location_text:
                # Update items
                self._current_dir = self._location_text
                self._selected = str()
                self._items = self.list_items(self._current_dir, self._show_hidden)

            for item in self._items:
                item_path = os.path.join(self._location_text, item)
                selected = item_path == self._selected

                if os.path.isfile(item_path):
                    if imgui.selectable(item, selected, DOUBLE_CLICK)[0]:
                        self._selected = item_path
                        if imgui.is_mouse_double_clicked(0):
                            imgui.close_current_popup()
                            return item_path
                elif os.path.isdir(item_path):
                    if imgui.selectable(item + "/", selected, DOUBLE_CLICK)[0]:
                        self._selected = item_path
                        if imgui.is_mouse_double_clicked(0):
                            self._location_text = item_path

        imgui.separator()

        if imgui.button(self._close_button_label):
            imgui.close_current_popup()
            return None

        imgui.same_line()

        select_file = os.path.isfile(self._selected)
        select_dir = os.path.isdir(self._selected)
        enabled_open = select_file or select_dir

        if button(self._open_button_label, disabled=not enabled_open):
            if select_file:
                imgui.close_current_popup()
                return self._selected
            elif select_dir:
                self._location_text = self._selected

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        if self._selected and pygame.key.get_pressed()[pygame.K_RETURN]:
            if select_file:
                imgui.close_current_popup()
                return self._selected
            elif select_dir:
                self._location_text = self._selected

        return None
