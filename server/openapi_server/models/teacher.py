from typing import List, Optional
from .meeting_summary import MeetingSummary
from pydantic import BaseModel, Field, EmailStr
from .time_interval import TimeInterval


class Teacher(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the teacher.")
    name: str = Field(..., description="Name of the teacher.")
    phone: Optional[str] = Field(None, description="Phone number of the teacher.")
    email: Optional[EmailStr] = Field(None, description="Email address of the teacher.")
    about_section: Optional[str] = Field(None, description="Short bio of the teacher.")
    available: List[TimeInterval] = Field(default_factory=list, description="List of available time intervals.")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Rating (0-5).")
    subjects_to_teach: List[str] = Field(default_factory=list, description="Subjects the teacher can teach.")
    hourly_rate: Optional[float] = Field(None, description="Hourly teaching rate.")
    meetings: List[MeetingSummary] = Field(default_factory=list, description="List of meetings.")

    class Config:
        schema_extra = {
            "example": {
                "id": "64d2f8f9e13f4c72a5d7df1e",
                "name": "Mr. Smith",
                "phone": "1234567890",
                "email": "mrsmith@example.com",
                "about_section": "Experienced history teacher.",
                "available": [
                    {
                        "start": "2024-12-13T10:00:00Z",
                        "end": "2024-12-13T12:00:00Z"
                    }
                ],

                "rating": 4.9,
                "subjects_to_teach": ["History", "Geography"],
                "hourly_rate": 50.0,
                "meetings": [{"meeting_id": "1234", "date": "2024-12-15T10:00:00Z"}],
            }
        }
