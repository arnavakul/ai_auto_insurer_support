from typing import Literal

from pydantic import BaseModel


class HeadDecision(BaseModel):

    next_action: Literal[
        "FILE",
        "VERIFY",
        "COST",
        "ORGANIZE",
        "ASK_USER",
        "END",
    ]

    reason: str