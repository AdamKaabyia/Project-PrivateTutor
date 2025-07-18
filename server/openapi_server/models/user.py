from typing import Optional, Union, List
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from .time_interval import TimeInterval


class User(BaseModel):
    """A model for representing a user in the system."""
    id: Optional[Union[str, ObjectId]] = Field(
        None, alias="_id", description="Unique identifier for the user (MongoDB ObjectId)."
    )
    username: str = Field(..., description="Unique username for the user.")
    email: EmailStr = Field(..., description="Email address of the user.")
    password: str = Field(..., description="Hashed password for authentication.")
    roles: List[str] = Field(
        default_factory=list, description="Roles assigned to the user (e.g., 'student', 'teacher')."
    )
    name: Optional[str] = Field(None, description="The full name of the user.")
    phone: Optional[str] = Field(None, description="The phone number of the user.")
    about_section: Optional[str] = Field(None, description="The 'About' section for the user.")
    available: Optional[List[TimeInterval]] = Field(
        default_factory=list, description="Availability times for meetings."
    )
    rating: Optional[float] = Field(None, description="Average rating, on a scale of 0 to 5.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp.")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,  # Serialize ObjectId as a string
        }
        populate_by_name = True
