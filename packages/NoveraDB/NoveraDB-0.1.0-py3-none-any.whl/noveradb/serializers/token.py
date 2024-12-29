"""Token serializers module."""
from datetime import UTC
from datetime import datetime
from datetime import timedelta

from uuid import UUID
from uuid import uuid4

from typing import List

from bson import ObjectId

from pydantic import Field
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import AwareDatetime

from .base import PyObjectId
from .base import DBTableBase
from .base import AllRecordsModel

TOKEN_EXPIRE_MINUTES = 60 * 24


class TokenInsertModel(BaseModel):
    """
    Container for a single Token Base record for insert.
    """

    # The primary key for the DoctorBaseModel, stored as a `str`
    # on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    user_id: PyObjectId
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": str(ObjectId())
            }
        },
    )


class TokenModel(TokenInsertModel, DBTableBase):
    """
    Container for a single Token record.
    """
    verification_token: UUID = Field(default_factory=uuid4)
    expire_time: AwareDatetime = Field(
        default=datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    model_config = ConfigDict(
        **{
            **DBTableBase.model_config,
            **TokenInsertModel.model_config,
            "populate_by_name": True,
            "json_schema_extra": {
                "example": {
                    **DBTableBase.model_config[
                        'json_schema_extra']['example'],
                    **TokenInsertModel.model_config[
                        'json_schema_extra']['example'],
                    "verification_token": str(uuid4()),
                    "expire_time": "2024-12-30T15:30:38.577171Z"
                }
            },
        }
    )


class TokenCollection(AllRecordsModel):
    """
    A container holding a list of `TokenModel` instances.

    This exists because providing a top-level array in a JSON
    response can be a
    [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    items: List[TokenModel]
