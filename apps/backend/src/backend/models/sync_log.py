from datetime import datetime
from pydantic import BaseModel
from datetime import timezone


class SyncLog(BaseModel):
    endpoint: str
    timestamp: str = datetime.now(timezone.utc).isoformat()
    status_code: int
