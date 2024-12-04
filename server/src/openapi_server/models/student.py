# coding: utf-8

"""
    Student-Teacher Meeting Scheduler API

    An API for scheduling meetings, managing persons, students, teachers, their ratings, and integrating with Google services. Additional endpoints allow managing teachers, students, and scheduling multi-participant meetings. 

    The version of the OpenAPI document: 1.4.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from openapi_server.models.meeting import Meeting
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Student(BaseModel):
    """
    Student
    """ # noqa: E501
    id: Optional[StrictInt] = None
    name: Optional[StrictStr] = None
    phone: Optional[StrictStr] = None
    email: Optional[StrictStr] = None
    about_section: Optional[StrictStr] = None
    available: Optional[List[datetime]] = None
    rating: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Average rating for the person, on a scale of 0 to 5.")
    subjects_interested_in_learning: Optional[List[StrictStr]] = None
    meetings: Optional[List[Meeting]] = None
    __properties: ClassVar[List[str]] = ["id", "name", "phone", "email", "about_section", "available", "rating", "subjects_interested_in_learning", "meetings"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Student from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in meetings (list)
        _items = []
        if self.meetings:
            for _item in self.meetings:
                if _item:
                    _items.append(_item.to_dict())
            _dict['meetings'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Student from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "phone": obj.get("phone"),
            "email": obj.get("email"),
            "about_section": obj.get("about_section"),
            "available": obj.get("available"),
            "rating": obj.get("rating"),
            "subjects_interested_in_learning": obj.get("subjects_interested_in_learning"),
            "meetings": [Meeting.from_dict(_item) for _item in obj.get("meetings")] if obj.get("meetings") is not None else None
        })
        return _obj


