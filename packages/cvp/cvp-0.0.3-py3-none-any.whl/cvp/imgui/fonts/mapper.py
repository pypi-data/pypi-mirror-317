# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from os import PathLike
from typing import Final, Optional, Union

import imgui

from cvp.imgui.fonts.builder import FontBuilder
from cvp.imgui.fonts.defaults import add_mdi_font, add_mixed_font
from cvp.imgui.fonts.font import Font


class FontMapper(OrderedDict[str, Font]):
    __normal_text_font_name__: Final[str] = "NormalText"
    __medium_text_font_name__: Final[str] = "MediumText"
    __large_text_font_name__: Final[str] = "LargeText"

    __normal_icon_font_name__: Final[str] = "NormalIcon"
    __medium_icon_font_name__: Final[str] = "MediumIcon"
    __large_icon_font_name__: Final[str] = "LargeIcon"

    def close(self):
        for font in self.values():
            font.close()

    @staticmethod
    def gen_font_key(name: str, size: int) -> str:
        return f"{name}, {size}px"

    def add_mixed_font(self, name: str, size: int, *, use_texture=False):
        if self.__contains__(name):
            raise KeyError(f"Already exists font key: {name}")

        font = add_mixed_font(name, size, use_texture=use_texture)
        self.__setitem__(name, font)
        return font

    def add_mixed_normal_text_font(self, size: int, *, use_texture=False):
        return self.add_mixed_font(
            name=self.__normal_text_font_name__,
            size=size,
            use_texture=use_texture,
        )

    def add_mixed_medium_text_font(self, size: int, *, use_texture=False):
        return self.add_mixed_font(
            name=self.__medium_text_font_name__,
            size=size,
            use_texture=use_texture,
        )

    def add_mixed_large_text_font(self, size: int, *, use_texture=False):
        return self.add_mixed_font(
            name=self.__large_text_font_name__,
            size=size,
            use_texture=use_texture,
        )

    @property
    def normal_text(self):
        return self.__getitem__(self.__normal_text_font_name__)

    @property
    def medium_text(self):
        return self.__getitem__(self.__medium_text_font_name__)

    @property
    def large_text(self):
        return self.__getitem__(self.__large_text_font_name__)

    def add_mdi_font(self, name: str, size: int, *, use_texture=False):
        if self.__contains__(name):
            raise KeyError(f"Already exists font key: {name}")

        font = add_mdi_font(name, size, use_texture=use_texture)
        self.__setitem__(name, font)
        return font

    def add_mdi_normal_icon_font(self, size: int, *, use_texture=False):
        return self.add_mdi_font(
            name=self.__normal_icon_font_name__,
            size=size,
            use_texture=use_texture,
        )

    def add_mdi_medium_icon_font(self, size: int, *, use_texture=False):
        return self.add_mdi_font(
            name=self.__medium_icon_font_name__,
            size=size,
            use_texture=use_texture,
        )

    def add_mdi_large_icon_font(self, size: int, *, use_texture=False):
        return self.add_mdi_font(
            name=self.__large_icon_font_name__,
            size=size,
            use_texture=use_texture,
        )

    @property
    def normal_icon(self):
        return self.__getitem__(self.__normal_icon_font_name__)

    @property
    def medium_icon(self):
        return self.__getitem__(self.__medium_icon_font_name__)

    @property
    def large_icon(self):
        return self.__getitem__(self.__large_icon_font_name__)

    def add_ttf(
        self,
        filepath: Union[str, PathLike[str]],
        size: int,
        *,
        name: Optional[str] = None,
        use_texture=False,
    ):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: '{str(filepath)}'")

        if not name:
            name = os.path.basename(filepath)

        assert isinstance(name, str)

        builder = FontBuilder(name, size)
        builder.add_ttf(filepath)
        font = builder.done(use_texture=use_texture)

        self.__setitem__(name, font)
        return font

    def add_normal_ttf(
        self,
        filepath: Union[str, PathLike[str]],
        size: int,
        *,
        use_texture=False,
    ):
        return self.add_ttf(
            filepath=filepath,
            size=size,
            name=self.__normal_text_font_name__,
            use_texture=use_texture,
        )

    def add_medium_ttf(
        self,
        filepath: Union[str, PathLike[str]],
        size: int,
        *,
        use_texture=False,
    ):
        return self.add_ttf(
            filepath=filepath,
            size=size,
            name=self.__medium_text_font_name__,
            use_texture=use_texture,
        )

    def add_large_ttf(
        self,
        filepath: Union[str, PathLike[str]],
        size: int,
        *,
        use_texture=False,
    ):
        return self.add_ttf(
            filepath=filepath,
            size=size,
            name=self.__large_text_font_name__,
            use_texture=use_texture,
        )

    @staticmethod
    def get_font_global_scale() -> float:
        return imgui.get_io().font_global_scale

    @staticmethod
    def set_font_global_scale(scale: float) -> None:
        imgui.get_io().font_global_scale = scale

    @property
    def font_global_scale(self) -> float:
        return self.get_font_global_scale()

    @font_global_scale.setter
    def font_global_scale(self, scale: float) -> None:
        self.set_font_global_scale(scale)
