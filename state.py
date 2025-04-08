from typing import TypedDict, Optional

class NegotiationState(TypedDict):
    cpm: int
    user_message: str
    message: str
    history: list[str]
    offer_type: Optional[str]
    final_price: Optional[float]
    final_format: Optional[str]
    agreed: bool
    rejected: bool
    price_drop_count: int
    cpm: Optional[float]
    min_views: Optional[int]
    max_views: Optional[int]


user_states: dict[int, NegotiationState] = {}