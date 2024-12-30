# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import PathLike
from typing import Optional, Union

from type_serialize import deserialize, serialize
from yaml import dump, full_load

from cvp.flow.catalog import FlowCatalog
from cvp.flow.datas.action import Action
from cvp.flow.datas.graph import Graph
from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin
from cvp.flow.datas.stream import Stream
from cvp.flow.path import FlowPath
from cvp.resources.home import HomeDir
from cvp.strings.is_uuid import is_uuid4
from cvp.yaml.dumpers import IndentListDumper


class FlowManager(OrderedDict[str, Graph]):
    def __init__(self, home: HomeDir, *, cursor: Optional[str] = None, update=False):
        super().__init__()
        self._catalog = FlowCatalog.from_builtins()
        self._home = home
        self._cursor = cursor
        if update:
            self.refresh_flow_graphs()

    def refresh_flow_graphs(self):
        for file in self._home.flows.find_graph_files():
            self.update_graph_yaml(file)

    @property
    def catalog(self):
        return self._catalog

    @property
    def opened(self):
        return bool(self._cursor)

    @property
    def cursor(self):
        return self._cursor

    @property
    def current_graph(self) -> Optional[Graph]:
        if self._cursor is None:
            return None
        return self.get(self._cursor, None)

    def open_graph(self, uuid: str) -> None:
        if uuid not in self:
            raise KeyError(f"Not exists flow graph: '{uuid}'")

        if self._cursor:
            raise ValueError("The graph is already opened")

        assert self._cursor is None
        self._cursor = uuid

    def close_graph(self) -> None:
        if not self._cursor:
            raise ValueError("The graph is already closed")

        assert isinstance(self._cursor, str)
        self._cursor = None

    def open_graph_safely(self, uuid: str) -> None:
        if self.opened:
            self.close_graph()

        assert not self.opened
        self.open_graph(uuid)

    # noinspection PyShadowingBuiltins
    def create_graph(
        self,
        name: str,
        *,
        template: Optional[str] = None,
        append=False,
        open=False,
    ) -> Graph:
        if not append and open:
            raise ValueError("If you don't append a graph, you can't select it")

        template = template if template else str()
        assert isinstance(template, str)
        graph = Graph(name=name)
        assert is_uuid4(graph.uuid)

        if append:
            assert graph.uuid
            assert graph.uuid not in self
            self[graph.uuid] = graph

        if open:
            self._cursor = graph.uuid

        return graph

    def remove_graph(self, uuid: str) -> Graph:
        if uuid == self._cursor:
            raise KeyError(f"The selected graph cannot be removed: '{uuid}'")
        if uuid in self:
            raise KeyError(f"Not exists flow graph: '{uuid}'")
        return self.pop(uuid)

    @staticmethod
    def dumps_graph_yaml(graph: Graph, encoding="utf-8") -> bytes:
        return dump(serialize(graph), Dumper=IndentListDumper).encode(encoding)

    @staticmethod
    def loads_graph_yaml(data: bytes) -> Graph:
        result = deserialize(full_load(data), Graph)
        assert isinstance(result, Graph)
        return result

    @staticmethod
    def write_graph_yaml(
        filepath: Union[str, PathLike[str]],
        graph: Graph,
        encoding="utf-8",
    ) -> None:
        with open(filepath, "wb") as f:
            f.write(FlowManager.dumps_graph_yaml(graph, encoding=encoding))

    @staticmethod
    def read_graph_yaml(filepath: Union[str, PathLike[str]]) -> Graph:
        with open(filepath, "rb") as f:
            return FlowManager.loads_graph_yaml(f.read())

    def update_graph_yaml(self, filepath: Union[str, PathLike[str]]) -> None:
        graph = self.read_graph_yaml(filepath)
        if not graph.uuid:
            raise ValueError("The 'uuid' of the flow graph does not exist")
        self[graph.uuid] = graph

    def get_node_template(self, path: Union[str, FlowPath]):
        return self._catalog.get_node_template(path)

    def add_node(self, path: Union[str, FlowPath]) -> Node:
        graph = self.current_graph
        if graph is None:
            raise LookupError("A graph must be selected")

        node_template = self.get_node_template(path)
        node_name = node_template.name
        node_docs = node_template.docs
        node_emblem = node_template.emblem
        node_color = node_template.color

        flow_inputs = list()
        flow_outputs = list()

        data_inputs = list()
        data_outputs = list()

        for pin_template in node_template.pins:
            pin = Pin(
                name=pin_template.name,
                docs=pin_template.docs,
                dtype=pin_template.dtype,
                action=pin_template.action,
                stream=pin_template.stream,
                required=pin_template.required,
            )

            if pin.action == Action.flow and pin.stream == Stream.input:
                flow_inputs.append(pin)
            elif pin.action == Action.flow and pin.stream == Stream.output:
                flow_outputs.append(pin)
            elif pin.action == Action.data and pin.stream == Stream.input:
                data_inputs.append(pin)
            elif pin.action == Action.data and pin.stream == Stream.output:
                data_outputs.append(pin)
            else:
                assert False, "Inaccessible section"

        node = Node(
            name=node_name,
            docs=node_docs,
            emblem=node_emblem,
            color=node_color,
            flow_inputs=flow_inputs,
            flow_outputs=flow_outputs,
            data_inputs=data_inputs,
            data_outputs=data_outputs,
        )

        graph.nodes.append(node)
        return node
