# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Tuple

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.palette.basic import RED, WHITE
from cvp.types.colors import RGBA
from cvp.variables import (
    DEFAULT_API_SELECT_WIDTH,
    DEFAULT_FONT_SCALE,
    DEFAULT_LARGE_ICON_FONT_SIZE,
    DEFAULT_LARGE_TEXT_FONT_SIZE,
    DEFAULT_MEDIUM_ICON_FONT_SIZE,
    DEFAULT_MEDIUM_TEXT_FONT_SIZE,
    DEFAULT_NORMAL_ICON_FONT_SIZE,
    DEFAULT_NORMAL_TEXT_FONT_SIZE,
    MAX_API_SELECT_WIDTH,
    MIN_API_SELECT_WIDTH,
)


@dataclass
class FontConfig:
    user_font: str = field(default_factory=str)
    scale: float = DEFAULT_FONT_SCALE
    normal_text_size: int = DEFAULT_NORMAL_TEXT_FONT_SIZE
    medium_text_size: int = DEFAULT_MEDIUM_TEXT_FONT_SIZE
    large_text_size: int = DEFAULT_LARGE_TEXT_FONT_SIZE
    normal_icon_size: int = DEFAULT_NORMAL_ICON_FONT_SIZE
    medium_icon_size: int = DEFAULT_MEDIUM_ICON_FONT_SIZE
    large_icon_size: int = DEFAULT_LARGE_ICON_FONT_SIZE
    load_all: bool = False

    @property
    def normal_text_size_pixels(self):
        return self.normal_text_size * self.scale

    @property
    def medium_text_size_pixels(self):
        return self.medium_text_size * self.scale

    @property
    def large_text_size_pixels(self):
        return self.large_text_size * self.scale

    @property
    def normal_icon_size_pixels(self):
        return self.normal_icon_size * self.scale

    @property
    def medium_icon_size_pixels(self):
        return self.medium_icon_size * self.scale

    @property
    def large_icon_size_pixels(self):
        return self.large_icon_size * self.scale


@dataclass
class FontManagerConfig(ManagerWindowConfig):
    range_select_width: float = DEFAULT_API_SELECT_WIDTH
    min_range_select_width: float = MIN_API_SELECT_WIDTH
    max_range_select_width: float = MAX_API_SELECT_WIDTH
    selected_block: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    text_color: RGBA = field(default_factory=lambda: (*WHITE, 1.0))
    normal_stroke_color: RGBA = field(default_factory=lambda: (*WHITE, 0.3))
    error_stroke_color: RGBA = field(default_factory=lambda: (*RED, 0.3))
    rounding: float = 0.0
    rect_flags: int = 0
    thickness: float = 1.0
    padding: float = 4.0
