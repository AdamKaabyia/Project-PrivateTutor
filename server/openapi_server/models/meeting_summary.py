from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MeetingSummary(BaseModel):
    meeting_id: Optional[str] = Field(..., description="Meeting identifier")
    date: Optional[datetime] = Field(..., description="Meeting date")

    class Config:
        schema_extra = {
            "example": {
                "meeting_id": "64d2f8f9e13f4c72a5d7df1e",
                "date": "2025-07-10T14:00:00Z"
            }
        }
