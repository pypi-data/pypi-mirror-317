# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from cvp.config.sections.bases.sidebar import SidebarWindowConfig


@dataclass
class ManagerWindowConfig(SidebarWindowConfig):
    selected: str = field(default_factory=str)
