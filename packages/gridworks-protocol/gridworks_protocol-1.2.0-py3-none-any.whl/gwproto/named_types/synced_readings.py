"""Type synced.readings, version 000"""

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, StrictInt, model_validator
from typing_extensions import Self

from gwproto.property_format import (
    SpaceheatName,
    UTCMilliseconds,
)


class SyncedReadings(BaseModel):
    ChannelNameList: List[SpaceheatName]
    ValueList: List[StrictInt]
    ScadaReadTimeUnixMs: UTCMilliseconds
    TypeName: Literal["synced.readings"] = "synced.readings"
    Version: Literal["000"] = "000"

    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="after")
    def check_axiom_1(self) -> Self:
        """
        Axiom 1: List Length Consistency.
        len(ChannelNameList) = len(ValueList)
        """
        # Implement check for axiom 1"
        return self
