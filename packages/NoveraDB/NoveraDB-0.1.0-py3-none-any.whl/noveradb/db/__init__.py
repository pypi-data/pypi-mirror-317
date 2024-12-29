import os

import motor.motor_asyncio


def get_mongodb_uri():
    """
    Get URI.

    Get the mongodb uri to connect to database.
    """
    return os.getenv(
        "NOVERA_DB_CONN_STR",
        "mongodb://user:pass@127.0.0.1:27017"
    )


def get_client():
    """
    Get Client.

    Get the client for the database connection.
    """
    return motor.motor_asyncio.AsyncIOMotorClient(
        get_mongodb_uri(),
        uuidRepresentation='standard',
        tz_aware=True,
    )


def get_db_name():
    return os.getenv(
        'NOVERA_DB_DATABASE_NAME',
        'novera')


async def get_session():
    client = get_client()
    async with await client.start_session() as session:
        async with session.start_transaction():
            return session
