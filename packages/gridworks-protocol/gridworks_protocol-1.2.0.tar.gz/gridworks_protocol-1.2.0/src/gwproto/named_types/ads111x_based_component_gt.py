"""Type ads111x.based.component.gt, version 000"""

from typing import List, Literal

from pydantic import ConfigDict, field_validator

from gwproto.named_types.ads_channel_config import (
    AdsChannelConfig,
)
from gwproto.named_types.component_gt import ComponentGt
from gwproto.property_format import (
    check_is_near5,
)


class Ads111xBasedComponentGt(ComponentGt):
    OpenVoltageByAds: List[float]
    ConfigList: List[AdsChannelConfig]
    TypeName: Literal["ads111x.based.component.gt"] = "ads111x.based.component.gt"
    Version: Literal["000"] = "000"

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("OpenVoltageByAds")
    @classmethod
    def _check_open_voltage_by_ads(cls, v: List[float]) -> List[float]:
        try:
            for elt in v:
                check_is_near5(elt)
        except ValueError as e:
            raise ValueError(
                f"OpenVoltageByAds element failed Near5 format validation: {e}",
            ) from e
        return v

    @field_validator("ConfigList")
    @classmethod
    def check_config_list(cls, v: List[AdsChannelConfig]) -> List[AdsChannelConfig]:
        """
            Axiom 1: Terminal Block consistency and Channel Name uniqueness.
            Terminal Block consistency and Channel Name uniqueness. - Each TerminalBlockIdx occurs at
        most once in the ConfigList .Each data channel occurs at most once in the ConfigList
        """
        # Implement Axiom(s)
        return v
