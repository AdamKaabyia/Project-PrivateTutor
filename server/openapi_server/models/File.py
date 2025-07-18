from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class File(BaseModel):
    file_name: str
    file_type: str
    file_path: Optional[str] = None
    file_content: Optional[bytes] = None
    owner_id: Optional[int] = None
    upload_date: datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True  # Allow types like `bytes` if needed

    def to_dict(self):
        """
        Serializes the File object to a dictionary.
        """
        return self.model_dump()


    @classmethod
    def from_dict(cls, data):
        """
        Deserializes a dictionary into a File object.
        """
        return cls(**data)

    def __str__(self):
        """
        String representation of the File object.
        """
        return f"File(name={self.file_name}, type={self.file_type}, owner={self.owner_id}, upload_date={self.upload_date})"
