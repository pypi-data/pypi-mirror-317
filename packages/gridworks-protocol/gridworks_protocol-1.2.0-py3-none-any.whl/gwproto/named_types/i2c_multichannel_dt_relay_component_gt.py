"""Type i2c.multichannel.dt.relay.component.gt, version 000"""

from typing import List, Literal

from pydantic import ConfigDict, StrictInt, model_validator
from typing_extensions import Self

from gwproto.named_types.component_gt import ComponentGt
from gwproto.named_types.relay_actor_config import RelayActorConfig


class I2cMultichannelDtRelayComponentGt(ComponentGt):
    I2cAddressList: List[StrictInt]
    ConfigList: List[RelayActorConfig]
    TypeName: Literal["i2c.multichannel.dt.relay.component.gt"] = (
        "i2c.multichannel.dt.relay.component.gt"
    )
    Version: Literal["001"] = "001"

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    @model_validator(mode="after")
    def check_axiom_3(self) -> Self:
        """g
        Axiom 2: Actor and Idx Consistency.
        There are no duplicates of ActorName or RelayIdx in the RelayConfigList
        """
        # Implement Axiom(s)
        return self
