# -*- coding: utf-8 -*-

from dataclasses import dataclass

from cvp.config.sections.bases.manager import ManagerWindowConfig
from cvp.variables import PROCESS_TEARDOWN_TIMEOUT


@dataclass
class ProcessManagerConfig(ManagerWindowConfig):
    teardown_timeout: float = PROCESS_TEARDOWN_TIMEOUT
