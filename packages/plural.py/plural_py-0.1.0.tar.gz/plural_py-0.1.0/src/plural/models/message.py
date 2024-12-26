from datetime import datetime

from .abc import PluralModel


class Message(PluralModel):
    original_id: int | None
    """The original message ID before it was proxied. This will be `None` if the message was sent through the API."""
    proxy_id: int
    """The proxied message ID."""
    author_id: int
    """The Discord ID of the user that sent the message."""
    channel_id: int
    """The Discord ID of the channel where the message was sent."""
    reason: str
    """The reason the message was proxied."""
    timestamp: datetime
    """The timestamp when the message was proxied."""
