# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.context.context import Context
from cvp.flow.datas.arc import Arc
from cvp.flow.datas.axis import Axis
from cvp.flow.datas.graph import Graph
from cvp.flow.datas.grid import Grid
from cvp.flow.datas.line_type import (
    LINE_TYPE_INDEX2NAME,
    LINE_TYPE_NAME2INDEX,
    LINE_TYPE_NAMES,
    LineType,
)
from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin
from cvp.flow.datas.selected_items import SelectedItems
from cvp.flow.datas.stroke import Stroke
from cvp.flow.datas.style import Style
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.combo import combo
from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.fonts.mapper import FontMapper
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_var import style_disable_input
from cvp.types.override import override
from cvp.widgets.tab import TabItem

INPUT_BUFFER: Final[int] = 256
ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE


class PropsTab(TabItem[Graph]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(context, "Props")
        self._fonts = fonts

    @override
    def on_item(self, item: Graph) -> None:
        selected_items = item.selected_items
        selected_nodes = selected_items.nodes
        selected_pins = selected_items.pins
        selected_arcs = selected_items.arcs

        if len(selected_items) == 0:
            self.on_graph_cursor(item)
        elif len(selected_items) == 1:
            if selected_items.nodes:
                assert 1 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 0 == len(selected_arcs)
                self.on_node_item(selected_nodes[0])
            elif selected_items.pins:
                assert 0 == len(selected_nodes)
                assert 1 == len(selected_pins)
                assert 0 == len(selected_arcs)
                self.on_pin_item(selected_pins[0])
            elif selected_items.arcs:
                assert 0 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 1 == len(selected_arcs)
                self.on_arc_item(item, selected_arcs[0])
            else:
                assert False, "Inaccessible section"
        else:
            assert 2 <= len(selected_items)
            self.on_multiple_items(item, selected_items)

    @staticmethod
    def tree_grid(label: str, grid: Grid) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", grid.visible):
                    grid.visible = visible.state
                if step := input_float("Step", grid.step):
                    grid.step = step.value
                if thickness := input_float("Thickness", grid.thickness):
                    grid.thickness = thickness.value
                if color := color_edit4("Color", *grid.color):
                    grid.color = color.color
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_axis(label: str, axis: Axis) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", axis.visible):
                    axis.visible = visible
                if thickness := input_float("Thickness", axis.thickness):
                    axis.thickness = thickness.value
                if color := color_edit4("Color", *axis.color):
                    axis.color = color.color
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_stroke(label: str, stroke: Stroke) -> None:
        if imgui.tree_node(label):
            try:
                if color := color_edit4("Color", *stroke.color):
                    stroke.color = color.color
                if thickness := input_float("Thickness", stroke.thickness):
                    stroke.thickness = thickness.value
                if rounding := input_float("Rounding", stroke.rounding):
                    stroke.rounding = rounding.value
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_style_colors(label: str, style: Style) -> None:
        if imgui.tree_node(label):
            try:
                if color := color_edit4("Normal", *style.normal_color):
                    style.normal_color = color.color
                if color := color_edit4("Hovering", *style.hovering_color):
                    style.hovering_color = color.color
                if color := color_edit4("Layout", *style.layout_color):
                    style.layout_color = color.color
            finally:
                imgui.tree_pop()

    def on_graph_cursor(self, graph: Graph) -> None:
        input_text_disabled("Type", "Graph")
        input_text_disabled("UUID", graph.uuid)

        graph.name = input_text_value("Name", graph.name)
        graph.docs = input_text_value("Docs", graph.docs)

        if color_result := color_edit4("Color", *graph.color):
            graph.color = color_result.color

        self.tree_grid("Grid X", graph.grid_x)
        self.tree_grid("Grid Y", graph.grid_y)
        self.tree_axis("Axis X", graph.axis_x)
        self.tree_axis("Axis Y", graph.axis_y)
        self.tree_stroke("Selected node", graph.style.selected_node)
        self.tree_stroke("Hovering node", graph.style.hovering_node)
        self.tree_stroke("Normal node", graph.style.normal_node)
        self.tree_style_colors("Colors", graph.style)

        if show_layout := checkbox("Show layout", graph.style.show_layout):
            graph.style.show_layout = show_layout.state

    @staticmethod
    def tree_node_debugging(label: str, node: Node) -> None:
        if imgui.tree_node(label):
            try:
                message = node.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def on_node_item(self, node: Node) -> None:
        input_text_disabled("Type", type(node).__name__)
        input_text_disabled("UUID", node.uuid)

        node.name = input_text_value("Name", node.name)
        node.docs = input_text_value("Docs", node.docs)

        with self._fonts.normal_icon:
            input_text_disabled("Emblem", node.emblem)

        if color_result := color_edit4("Color", *node.color):
            node.color = color_result.color

        if self.context.debug:
            self.tree_node_debugging("Debugging", node)

        # flow_inputs: List[Pin] = field(default_factory=list)
        # flow_outputs: List[Pin] = field(default_factory=list)
        # data_inputs: List[Pin] = field(default_factory=list)
        # data_outputs: List[Pin] = field(default_factory=list)

    @staticmethod
    def tree_pin_debugging(label: str, pin: Pin) -> None:
        if imgui.tree_node(label):
            try:
                message = pin.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def on_pin_item(self, pin: Pin) -> None:
        input_text_disabled("Type", type(pin).__name__)
        input_text_disabled("Name", pin.name)
        input_text_disabled("Data Type", pin.dtype)
        input_text_disabled("Action", str(pin.action))
        input_text_disabled("Stream", str(pin.stream))

        with style_disable_input():
            checkbox("Required", pin.required)

        if self.context.debug:
            self.tree_pin_debugging("Debugging", pin)

    def on_arc_item(self, graph: Graph, arc: Arc) -> None:
        input_text_disabled("Type", type(arc).__name__)
        input_text_disabled("UUID", arc.uuid)

        arc.name = input_text_value("Name", arc.name)
        arc.docs = input_text_value("Docs", arc.docs)

        line_index = LINE_TYPE_NAME2INDEX[str(arc.line_type)]
        if line_result := combo("Line Type", line_index, LINE_TYPE_NAMES):
            line_name = LINE_TYPE_INDEX2NAME[line_result.value]
            arc.line_type = LineType(line_name)
            graph.update_arc_polyline(arc, force=True)

        sax, say = arc.start_anchor.point
        if anchor_result := drag_float2("Start Anchor", sax, say):
            arc.start_anchor.point = anchor_result.values
            graph.update_arc_polyline(arc, force=True)

        eax, eay = arc.end_anchor.point
        if anchor_result := drag_float2("End Anchor", eax, eay):
            arc.end_anchor.point = anchor_result.values
            graph.update_arc_polyline(arc, force=True)

        if arc.output:
            if imgui.tree_node("Output pin"):
                try:
                    self.on_pin_item(arc.output.pin)
                finally:
                    imgui.tree_pop()

        if arc.input:
            if imgui.tree_node("Input pin"):
                try:
                    self.on_pin_item(arc.input.pin)
                finally:
                    imgui.tree_pop()

    def on_multiple_items(self, graph: Graph, items: SelectedItems) -> None:
        input_text_disabled("Type", "Multiple")

        for key, item in items.items():
            typename = type(item).__name__
            title = f"{typename} ({item.name})" if item.name else typename
            label = f"{title}###{key}"
            if imgui.tree_node(label):
                try:
                    if isinstance(item, Node):
                        self.on_node_item(item)
                    elif isinstance(item, Pin):
                        self.on_pin_item(item)
                    elif isinstance(item, Arc):
                        self.on_arc_item(graph, item)
                    else:
                        assert False, "Inaccessible section"
                finally:
                    imgui.tree_pop()
