from typing import Any, Literal, NamedTuple

ActionType = Literal["send", "receive"]

class HistoryAction(NamedTuple):
    action_type: ActionType
    usd_amount: str
    message: str | None
    link: str | None

    def to_json(self) -> dict[str, Any]:
        return {
            'action_type': self.action_type,
            'usd_amount': self.usd_amount,
            'message': self.message,
            'link': self.link
        }


class TokenInfo(NamedTuple):
    decimals: int
    symbol: str
    coingecko: str
