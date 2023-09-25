

from datetime import datetime, timezone
from pydantic import UUID4, BaseModel


class ChatMessage(BaseModel):
    uid: UUID4
    from_id: UUID4
    to_id: UUID4
    timestamp: datetime
    tz: timezone
    body: str