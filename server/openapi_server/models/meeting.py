from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime

from .person import Person
from .File import File

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)
class Meeting(BaseModel):
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    finish_time: Optional[datetime] = None
    subject: Optional[str] = None
    people: List[Person] = []
    attached_files: List[File] = []

    class Config:
        schema_extra = {
            'example': {
                'location': "Conference Room A",
                'start_time': "2022-01-01T09:00:00Z",
                'finish_time': "2022-01-01T10:00:00Z",
                'subject': "Budget Meeting",
                'people': [{
                    'name': "John Doe",
                    'email': "johndoe@example.com"
                }],
                'attached_files': [{
                    'filename': "agenda.pdf",
                    'url': "http://example.com/agenda.pdf"
                }]
            }
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Meeting':
        """Returns the dict as a model, ensuring types are correct."""
        return cls(**dikt)

    class Config:
        arbitrary_types_allowed = True

