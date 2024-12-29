"""Base serializers."""

from typing import Annotated

from bson import ObjectId

from pydantic import Field
from pydantic import BaseModel
from pydantic import ConfigDict

from pydantic.functional_validators import BeforeValidator

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can
# be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class PaginationModel(BaseModel):
    page: int = Field(gt=0, default=1)
    per_page: int = Field(gt=0, default=10)


class AllRecordsModel(PaginationModel):
    total: int = Field(gt=0, default=0)


class DBTableBase(BaseModel):
    # The primary key for the Table, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: PyObjectId | None = Field(alias="_id",
                                  serialization_alias="id",
                                  default=None)
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "id": "OBJECT_ID"
            }
        },
    )
