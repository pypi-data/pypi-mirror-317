from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Callable, TypeAlias


if TYPE_CHECKING:
    pass

MqttCallback: TypeAlias = Callable[[str, str], None]
