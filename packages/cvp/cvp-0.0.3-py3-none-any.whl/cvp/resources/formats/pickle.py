# -*- coding: utf-8 -*-

import pickle
from os import PathLike
from typing import Any, Final, Union

from cvp.resources.formats._base import BaseFormatPath
from cvp.types.override import override

PICKLE_PROTOCOL_VERSION: Final[int] = 5
PICKLE_ENCODING: Final[str] = "ASCII"


class PickleFormatPath(BaseFormatPath):
    def __init__(self, path: Union[str, PathLike[str]]):
        super().__init__(path, suffix=".pickle")
        self._pickle_protocol_version = PICKLE_PROTOCOL_VERSION
        self._pickle_encoding = PICKLE_ENCODING

    @override
    def dumps(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self._pickle_protocol_version)

    @override
    def loads(self, data: bytes) -> Any:
        return pickle.loads(data, encoding=self._pickle_encoding)
