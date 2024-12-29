"""Doctor collection."""
from typing import Any
from typing import Dict

from bson import ObjectId
from bson.errors import InvalidId

from motor.motor_asyncio import AsyncIOMotorDatabase
from motor.motor_asyncio import AsyncIOMotorClientSession

from noveradb.db import get_db_name

COLLECTION_NAME = 'doctor'


async def create_indexes(session: AsyncIOMotorClientSession):
    """
    Create indexes.

    Args:
        session (AsyncIOMotorClientSession): Database session.

    """
    collection = session.client[get_db_name()][COLLECTION_NAME]
    await collection.create_index(
        "email",
        name="email_index",
        unique=True
    )


async def get_doctor(doctor_id: str,
                     session: AsyncIOMotorClientSession) -> Dict[str, Any]:
    """
    Get the record for a specific doctor, looked up by `doctor_id`.

    Args:
        doctor_id (str): Doctor id.
        session (AsyncIOMotorClientSession): Database session.

    Raises:
        TypeError: If the user_id is not valid.
        ValueError: If doctor not exists.

    Returns:
        dict: Client record.

    """
    ret_val = {}
    # Check if its valid ObjectId or not
    try:
        id_: ObjectId = ObjectId(doctor_id)
    except InvalidId:
        raise TypeError("Invalid doctor_id, it need bson.ObjectId.")
    else:
        collection: AsyncIOMotorDatabase = \
            session.client[get_db_name()][COLLECTION_NAME]

        if (
            ret_val := await collection.find_one({"_id": id_})
        ) is None:
            raise ValueError(f"Doctor with '{doctor_id}' id not exists")

    return ret_val
