# -*- coding: utf-8 -*-

from cvp.context.context import Context
from cvp.flow.datas.templates.graph import GraphTemplate
from cvp.imgui.fonts.mapper import FontMapper
from cvp.widgets.tab import TabBar
from cvp.windows.flow.left.graphs import GraphsTab
from cvp.windows.flow.left.tree import TreeTab


class FlowLeftTabs(TabBar[GraphTemplate]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(
            context=context,
            identifier="## FlowLeftTabs",
            flags=0,
        )
        self.register(TreeTab(context, fonts))
        self.register(GraphsTab(context))
