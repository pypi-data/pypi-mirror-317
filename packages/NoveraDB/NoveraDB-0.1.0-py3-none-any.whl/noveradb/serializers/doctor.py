"""Doctor serializers module."""
import re

from enum import Enum

from datetime import UTC
from datetime import datetime

#  from uuid import UUID
#  from uuid import uuid4

from typing import List

from bson import ObjectId

from pydantic import Field
from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import AwareDatetime
from pydantic import field_validator

from pydantic_extra_types.country import CountryAlpha3
from pydantic_extra_types.phone_numbers import PhoneNumber

from .base import DBTableBase
from .base import AllRecordsModel


class StatusEnum(str, Enum):
    pending = 'pending'
    verify_email_sent = 'verify_email_sent'
    email_verified = 'email_verified'
    active = 'active'


class DoctorInsertModel(BaseModel):
    """
    Container for a single Doctor Base record for insert.
    """

    # The primary key for the DoctorBaseModel, stored as a `str`
    # on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    last_name: str = Field(min_length=2)
    first_name: str = Field(min_length=2)
    email: EmailStr
    phone: PhoneNumber
    country: CountryAlpha3
    password: str = Field(min_length=8)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "first_name": "Mohamed",
                "last_name": "Azzabi",
                "email": "mohamed@novera.com",
                "phone": "+911234567890",
                "country": "ARE",
                "password": "PAssword@123",
            }
        },
    )

    @field_validator("password")
    def validate_password(cls, value):
        """
        Password validator with minumum length.
        """
        password_pattern = \
            r"^(?=(.*\d){2})(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z\d]).{,}$"

        if re.search(password_pattern, value):
            return value

        raise ValueError("Password must be combination of 2 digits, "
                         "capital and small letters with special characters.")


class DoctorUpdateModel(DoctorInsertModel):
    """
    Container for a single Doctor record for update.
    """

    # The primary key for the DoctorBaseModel, stored as
    # a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    last_name: str | None = Field(min_length=2, default=None)
    first_name: str | None = Field(min_length=2, default=None)
    email: EmailStr | None = None
    phone: PhoneNumber | None = None
    country: CountryAlpha3 | None = None
    password: str | None = Field(min_length=8, default=None)


class DoctorModel(DoctorInsertModel, DBTableBase):
    """
    Container for a single Doctor record.
    """
#   verification_token: UUID = Field(default_factory=uuid4)
    status: StatusEnum = Field(default=StatusEnum.pending)
    join_date: AwareDatetime = Field(
        default_factory=lambda: datetime.now(UTC))
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                **DBTableBase.model_config[
                     'json_schema_extra']['example'],
                **DoctorInsertModel.model_config[
                    'json_schema_extra']['example'],
                "status": "pending",
                "join_date": "2024-12-30T15:30:38.577171Z"
            }
        },
    )


class DoctorCollection(AllRecordsModel):
    """
    A container holding a list of `DoctorModel` instances.

    This exists because providing a top-level array in a JSON
    response can be a
    [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
    items: List[DoctorModel]
