"""Type fsm.full.report, version 000"""

from typing import List, Literal

from pydantic import BaseModel, ConfigDict

from gwproto.named_types.fsm_atomic_report import FsmAtomicReport
from gwproto.property_format import (
    SpaceheatName,
    UUID4Str,
)


class FsmFullReport(BaseModel):
    FromName: SpaceheatName
    TriggerId: UUID4Str
    AtomicList: List[FsmAtomicReport]
    TypeName: Literal["fsm.full.report"] = "fsm.full.report"
    Version: Literal["000"] = "000"

    model_config = ConfigDict(extra="allow", use_enum_values=True)
