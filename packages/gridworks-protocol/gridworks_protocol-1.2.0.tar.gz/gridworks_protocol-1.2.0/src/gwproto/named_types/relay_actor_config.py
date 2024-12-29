"""Type relay.actor.config, version 001"""

from typing import Literal

from pydantic import PositiveInt

from gwproto.enums import RelayWiringConfig
from gwproto.named_types import ChannelConfig
from gwproto.property_format import (
    SpaceheatName,
)


class RelayActorConfig(ChannelConfig):
    RelayIdx: PositiveInt
    ActorName: SpaceheatName
    WiringConfig: RelayWiringConfig
    EventType: str
    DeEnergizingEvent: str
    EnergizingEvent: str
    TypeName: Literal["relay.actor.config"] = "relay.actor.config"
    Version: Literal["001"] = "001"
