"""Type dfr.component.gt, version 000"""

from typing import List, Literal

from pydantic import PositiveInt

from gwproto.named_types import ComponentGt
from gwproto.named_types.dfr_config import DfrConfig


class DfrComponentGt(ComponentGt):
    ConfigList: List[DfrConfig]
    I2cAddressList: List[PositiveInt]
    TypeName: Literal["dfr.component.gt"] = "dfr.component.gt"
    Version: Literal["000"] = "000"
