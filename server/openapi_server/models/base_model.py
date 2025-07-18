from bson import ObjectId
from pydantic import BaseModel
from abc import ABC
from typing import Any, Dict, Type, TypeVar

T = TypeVar('T', bound='Model')


class Model(BaseModel, ABC):
    """Abstract base model providing common functionality for serialization."""

    class Config:
        # Allow population by field name or alias
        allow_population_by_field_name = True
        # Customize JSON serialization
        json_encoders = {
            # Add custom serialization logic if needed
            ObjectId: str
        }

    @classmethod
    def from_dict(cls: Type[T], dikt: Dict[str, Any]) -> T:
        """Deserialize a dictionary into a model instance."""
        return cls.parse_obj(dikt)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the model instance into a dictionary."""
        return self.dict(by_alias=True, exclude_unset=True)

    def to_str(self) -> str:
        """Return the string representation of the model."""
        return super().__str__()

    def __eq__(self, other: Any) -> bool:
        """Check equality between two model instances."""
        if isinstance(other, Model):
            return self.dict() == other.dict()
        return False

    def __ne__(self, other: Any) -> bool:
        """Check inequality between two model instances."""
        return not self.__eq__(other)
