from enum import Enum
from typing import Optional, TypedDict

from pydantic import BaseModel, Field


class OfferType(Enum):
    fixed = "Фиксированная"
    gap = 'С гэпом'

class Decision(Enum):
    accept = 'accept'
    reject = 'reject'


# class NegotiationState(BaseModel):
#     cpm: float = Field(default=0)
#     min_views: int = Field(default=0)
#     max_views: int = Field(default=0)
#
#     user_message: Optional[str] = Field(default='')
#     bot_message: Optional[str] = Field(default='')
#     propose_count: int = Field(default=1)
#
#     decision: str = Field(default='negotiation')
#     history: list[str] = Field(default=[])
#
#     current_offer: Optional[float] = Field(default=0)
#
#     finalize_message: Optional[str] = Field(default=None)
#     offer_type: Optional[OfferType] = Field(default=OfferType.fixed)
#
#     reason: Optional[str] = Field(default='')
#
#     awaiting_user_response: bool = Field(default=False)


class NegotiationState(TypedDict):
    cpm: float
    min_views: int
    max_views: int

    user_message: Optional[str]
    bot_message: Optional[str]

    propose_count: int

    decision: str
    history: list[str]

    current_offer: Optional[float]
    finalize_message: Optional[str]
    offer_type: Optional[OfferType]

    reason: Optional[str]

    awaiting_user_response: bool

    tg_id: int


user_states: dict[int, NegotiationState] = {}