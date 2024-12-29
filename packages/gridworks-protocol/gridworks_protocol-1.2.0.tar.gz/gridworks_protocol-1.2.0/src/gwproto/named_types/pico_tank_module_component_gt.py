"""Type pico.tank.reader.component.gt, version 000"""

from typing import Literal, Optional

from pydantic import ConfigDict, model_validator
from typing_extensions import Self

from gwproto.enums import TempCalcMethod
from gwproto.named_types.component_gt import ComponentGt


class PicoTankModuleComponentGt(ComponentGt):
    Enabled: bool
    PicoAHwUid: Optional[str] = None
    PicoBHwUid: Optional[str] = None
    TempCalcMethod: TempCalcMethod
    ThermistorBeta: int
    SendMicroVolts: bool
    Samples: int
    NumSampleAverages: int
    PicoKOhms: int
    SerialNumber: str = "NA"
    AsyncCaptureDeltaMicroVolts: int
    TypeName: Literal["pico.tank.module.component.gt"] = "pico.tank.module.component.gt"
    Version: Literal["000"] = "000"

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def check_axiom_2(self) -> Self:
        """
        Axiom 2: ConfigList stuff
        """
        return self
