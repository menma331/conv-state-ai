from enum import Enum
from typing import Optional, TypedDict

class OfferType(Enum):
    fixed = "Фиксированная"
    gap = 'С гэпом'

class Decision(Enum):
    accept = 'accept'
    reject = 'reject'

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


user_states: dict[int, NegotiationState] = {}