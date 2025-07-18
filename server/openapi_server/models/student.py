from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from .time_interval import TimeInterval


class Student(BaseModel):
    """Student model compatible with Pydantic and MongoDB."""

    id: Optional[str] = Field(
        None, description="Unique identifier for the student."
    )
    name: str = Field(..., description="Name of the student.")
    phone: Optional[str] = Field(None, description="Phone number of the student.")
    email: Optional[EmailStr] = Field(None, description="Email address of the student.")
    about_section: Optional[str] = Field(None, description="Short description or bio of the student.")
    available: List[TimeInterval] = Field(default_factory=list, description="List of available time intervals.")
    rating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Average rating for the student, on a scale of 0 to 5.",
    )
    subjects_interested_in_learning: Optional[List[str]] = Field(
        default_factory=list,
        description="List of subjects the student is interested in learning.",
    )
    meetings: Optional[List[dict]] = Field(
        default_factory=list,
        description="List of meetings associated with the student.",
    )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "64d2f8f9e13f4c72a5d7df1e",
                "name": "John Doe",
                "phone": "1234567890",
                "email": "johndoe@example.com",
                "about_section": "A curious learner passionate about technology.",
                "available": ["2024-12-13T10:00:00Z", "2024-12-14T15:00:00Z"],
                "rating": 4.5,
                "subjects_interested_in_learning": ["Math", "Physics", "Programming"],
                "meetings": [
                    {"meeting_id": "1234", "date": "2024-12-15T10:00:00Z"}
                ],
            }
        }
