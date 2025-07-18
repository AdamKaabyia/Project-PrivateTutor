from pydantic import BaseModel, Field, validator
from datetime import datetime


class TimeInterval(BaseModel):
    start: datetime = Field(..., description="Start time")
    end: datetime = Field(..., description="End time")

    @validator('end')
    def check_end_after_start(cls, end, values):
        start = values.get('start')
        if start and end <= start:
            raise ValueError("End time must be after start time")
        return end
