"""Type component.gt, version 001"""

from typing import List, Literal, Optional

from pydantic import BaseModel, field_validator

from gwproto.named_types.channel_config import ChannelConfig
from gwproto.property_format import UUID4Str


class ComponentGt(BaseModel):
    ComponentId: UUID4Str
    ComponentAttributeClassId: UUID4Str
    ConfigList: List[ChannelConfig]
    DisplayName: Optional[str] = None
    HwUid: Optional[str] = None
    TypeName: Literal["component.gt"] = "component.gt"
    Version: Literal["001"] = "001"

    @field_validator("ConfigList")
    @classmethod
    def check_config_list(cls, v: List[ChannelConfig]) -> List[ChannelConfig]:
        """
        Axiom 1: Channel Name uniqueness. Data Channel names are
        unique in the config list
        """
        # Implement Axiom(s)
        return v
