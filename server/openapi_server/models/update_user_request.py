from pydantic import BaseModel, EmailStr
from typing import Optional


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    about_section: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "phone": "555-1234",
                "about_section": "Loves teaching math",
            }
        }
