# coding: utf-8

"""
    Arthur Scope

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from scope_client.api_bindings.models.job_state import JobState
from typing import Optional, Set
from typing_extensions import Self

class JobRun(BaseModel):
    """
    JobRun
    """ # noqa: E501
    id: StrictStr = Field(description="The unique ID for the job run.")
    job_id: StrictStr = Field(description="The parent job for this job run.")
    state: JobState = Field(description="Current state of the job run.")
    job_attempt: StrictInt = Field(description="The attempt number of the job.")
    start_timestamp: datetime = Field(description="The timestamp this job run was started.")
    end_timestamp: Optional[datetime] = None
    __properties: ClassVar[List[str]] = ["id", "job_id", "state", "job_attempt", "start_timestamp", "end_timestamp"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of JobRun from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if end_timestamp (nullable) is None
        # and model_fields_set contains the field
        if self.end_timestamp is None and "end_timestamp" in self.model_fields_set:
            _dict['end_timestamp'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of JobRun from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "job_id": obj.get("job_id"),
            "state": obj.get("state"),
            "job_attempt": obj.get("job_attempt"),
            "start_timestamp": obj.get("start_timestamp"),
            "end_timestamp": obj.get("end_timestamp")
        })
        return _obj


