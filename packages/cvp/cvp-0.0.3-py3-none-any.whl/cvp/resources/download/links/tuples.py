# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Sequence, Tuple, Union
from urllib.parse import ParseResult

from cvp.hashfunc.checksum import Method
from cvp.variables import CHECKSUM_DELIMITER


class ExtractPair(NamedTuple):
    archive_path: str
    extract_path: str


class Checksum(NamedTuple):
    hash_method: Method
    hash_value: str

    def __str__(self) -> str:
        return f"{str(self.hash_method)}{CHECKSUM_DELIMITER}{self.hash_value}"

    @classmethod
    def parse(cls, method_value: str, delimiter=CHECKSUM_DELIMITER):
        method, value = method_value.split(delimiter, 1)
        assert isinstance(method, str)
        assert isinstance(value, str)
        return cls(Method(method.strip().lower()), value.strip())


class LinkInfo(NamedTuple):
    url: Union[str, ParseResult]
    paths: Sequence[Union[Tuple[str, str], ExtractPair]]
    checksum: Optional[Union[str, Tuple[str, str], Checksum]]
