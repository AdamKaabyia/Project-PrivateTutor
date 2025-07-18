from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union
from datetime import datetime


class Person(BaseModel):
    """A model for representing a person."""

    id: Optional[Union[str, ObjectId]] = Field(
        None, alias="_id", description="Unique identifier for the person (MongoDB ObjectId)."
    )
    name: Optional[str] = Field(None, description="The name of the person.")
    phone: Optional[str] = Field(None, description="The phone number of the person.")
    email: Optional[EmailStr] = Field(None, description="The email address of the person.")
    about_section: Optional[str] = Field(None, description="The 'About' section for the person.")
    available: Optional[List[datetime]] = Field(default_factory=list, description="Availability times.")
    rating: Optional[float] = Field(None, description="Average rating, on a scale of 0 to 5.")

    class Config:
        arbitrary_types_allowed = True  # Allow bson.ObjectId
        json_encoders = {
            ObjectId: str,  # Serialize ObjectId as a string
        }
        populate_by_name = True  # Allow alias resolution
