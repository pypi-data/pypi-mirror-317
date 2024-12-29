from abc import ABC, abstractmethod
from typing import NoReturn

from gwproto.data_classes.components.component import Component
from gwproto.data_classes.sh_node import ShNode


class ComponentResolver(ABC):
    @abstractmethod
    def resolve(
        self,
        node_name: str,
        nodes: dict[str, ShNode],
        components: dict[str, Component],
    ) -> NoReturn:
        raise NotImplementedError
