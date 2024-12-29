"""Token Collection."""
from datetime import UTC
from datetime import datetime

from typing import Any
from typing import Dict

from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClientSession

from noveradb.db import get_db_name
from noveradb.db.doctor import get_doctor

from noveradb.serializers.token import TokenModel
from noveradb.serializers.token import TokenInsertModel


COLLECTION_NAME = "token"


async def create_indexes(session: AsyncIOMotorClientSession):
    """
    Create indexes.

    Args:
        session (AsyncIOMotorClientSession): Database session.

    """
    collection = session.client[get_db_name()][COLLECTION_NAME]
    await collection.create_index(
        "verification_token",
        unique=True,
        name="verification_token_index",
    )


async def create_token(token_request: TokenInsertModel,
                       session: AsyncIOMotorClientSession,
                       validate_doctor: bool = True) -> Dict[str, Any]:
    """
    Insert a new token record.

    Args:
        token_request (TokenInsertModel): Token user data
        session (AsyncIOMotorClientSession): Database session.

    Kwargs:
        validate_doctor (bool)(default: True): Validate doctor data or not.

    Raises:
        TypeError: If the user_id is not valid.
        ValueError: If doctor not exists.

    Returns:
        dict: Newly created token.

    """

    if validate_doctor:
        # Check doctor exists.
        # This will raise `TypeError` and `ValueError`.
        get_doctor(token_request['user_id'], session)

    collection = session.client[get_db_name()][COLLECTION_NAME]
    data = {
        **token_request.model_dump(
            by_alias=True,
        ),
    }
    # Convert to doctor to get the default value for model
    token = TokenModel(**data)
    new_token = await collection.insert_one(
        token.model_dump(by_alias=True,
                         exclude="id")
    )
    created_token = await collection.find_one(
        {"_id": new_token.inserted_id}
    )
    return created_token


async def get_token_by_verify_token(
        verification_token: str,
        session: AsyncIOMotorClientSession,
        validate_expire_time: bool = True) -> Dict[str, Any]:
    """Get token by `verification_token`.

    Search the token data based on `verification_token`.

    Args:
        verification_token (str): UUID for the token.
        session (AsyncIOMotorClientSession): Database session.

    Raises:
        TypeError: If the `verification_token` is not valid UUID.
        NameError: If the `verification_token` is not found.
        ValueError: Token is expired.

    Returns:
        dict: Token record

    """

    ret_val: Dict[str, Any] = {}

    try:
        verification_uuid: UUID = UUID(verification_token)
    except ValueError:
        raise TypeError("Invalid token, it need UUID")
    else:
        collection = session.client[get_db_name()][COLLECTION_NAME]
        # Find token with valid expire time.
        if (
            ret_val := await collection.find_one(
                {"verification_token": verification_uuid}
            )
        ) is None:
            raise NameError(
                f"Token not exits with '{verification_token}' token")
        if validate_expire_time and ret_val['expire_time'] < datetime.now(UTC):
            raise ValueError("Token expired.")

    return ret_val
