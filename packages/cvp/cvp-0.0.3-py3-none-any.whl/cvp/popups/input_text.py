# -*- coding: utf-8 -*-

from typing import Callable, Optional

import imgui
import pygame

from cvp.imgui.button import button
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_item_width import item_width
from cvp.renderer.popup.base import PopupBase
from cvp.types.override import override
from cvp.variables import MIN_POPUP_TEXT_INPUT_HEIGHT, MIN_POPUP_TEXT_INPUT_WIDTH


class InputTextPopup(PopupBase[str]):
    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        text: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        centered=True,
        flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE,
        *,
        min_width=MIN_POPUP_TEXT_INPUT_WIDTH,
        min_height=MIN_POPUP_TEXT_INPUT_HEIGHT,
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

        self._label = label if label else str()
        self._text = text if text else str()
        self._ok_button_label = ok if ok else "Ok"
        self._cancel_button_label = cancel if cancel else "Cancel"
        self._text_label = "## Text"

    @property
    def text(self):
        return self._text

    @override
    def on_process(self) -> Optional[str]:
        if self._label:
            imgui.text(self._label)

        if imgui.is_window_appearing():
            imgui.set_keyboard_focus_here()

        with item_width(-1):
            self._text = input_text_value(self._text_label, self._text)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return self._text
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        if button(self._cancel_button_label):
            imgui.close_current_popup()
            return None
        imgui.same_line()
        if button(self._ok_button_label, disabled=not self._text):
            imgui.close_current_popup()
            return self._text

        return None
