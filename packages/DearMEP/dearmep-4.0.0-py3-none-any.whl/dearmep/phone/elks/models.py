# SPDX-FileCopyrightText: © 2023 iameru
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


InitialElkResponseState = Literal["ongoing", "success", "busy", "failed"]


class InitialCallElkResponse(BaseModel):
    callid: str = Field(alias="id")
    created: datetime
    direction: Literal["incoming", "outgoing"]
    state: InitialElkResponseState
    from_nr: str = Field(alias="from")
    to_nr: str = Field(alias="to")


class Number(BaseModel):
    category: Literal["fixed", "mobile", "voip"]
    country: str
    expires: datetime
    number: str
    capabilities: list[str]
    cost: int
    active: Literal["yes", "no"]
    allocated: datetime
    id: str
