# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.onvif import OnvifConfig
from cvp.context.context import Context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.types.override import override
from cvp.widgets.tab import TabItem

INPUT_BUFFER_SIZE: Final[int] = 2048


class OnvifInfoTab(TabItem[OnvifConfig]):
    def __init__(self, context: Context):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: OnvifConfig) -> None:
        input_text_disabled("UUID", item.uuid)
        item.name = input_text_value(
            "Name",
            item.name,
            INPUT_BUFFER_SIZE,
        )
        item.address = input_text_value(
            "Address",
            item.address,
            INPUT_BUFFER_SIZE,
        )

        ssl_verify = imgui.checkbox("No SSL Verify", item.no_verify)
        ssl_verify_changed = ssl_verify[0]
        ssl_verify_value = ssl_verify[1]
        assert isinstance(ssl_verify_changed, bool)
        assert isinstance(ssl_verify_value, bool)
        if ssl_verify_changed:
            item.no_verify = ssl_verify_value

        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text(
                    "Skip the certificate verification process."
                    " This may be a temporary solution if you get a"
                    " 'certificate verify failed' error."
                )

        same_host = imgui.checkbox("Same host", item.same_host)
        same_host_changed = same_host[0]
        same_host_value = same_host[1]
        assert isinstance(same_host_changed, bool)
        assert isinstance(same_host_value, bool)
        if same_host_changed:
            item.same_host = same_host_value

        if imgui.is_item_hovered():
            with imgui.begin_tooltip():
                imgui.text(
                    "Prevents WSDL addresses from being incorrect when accessing"
                    " ONVIF devices in environments such as proxy or tunneling."
                )
