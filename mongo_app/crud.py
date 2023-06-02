from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult
import exceptions


async def create_doc(
        data: dict,
        collection: Collection,
) -> InsertOneResult:
    try:
        doc: \
            InsertOneResult = \
            await collection.insert_one(data)
    except Exception as e:
        print(str(e))
        raise exceptions.MongoDBException(message=str(e))
    return doc


async def get_doc(
        data: dict,
        collection: Collection
) -> Cursor:
    try:
        doc: \
            Cursor = \
            await collection.find_one(data)
    except Exception as e:
        raise exceptions.MongoDBException(message=str(e))
    return doc


async def update_doc(
        query_data: dict,
        set_data: dict,
        collection: Collection,
) -> None:
    try:
        await collection.update_one(
            query_data,
            set_data,
        )
    except Exception as e:
        raise exceptions.MongoDBException(message=str(e))


async def update_docs(
        query_data: dict,
        set_data: dict,
        collection: Collection,
) -> None:
    try:
        await collection.update_many(
            query_data,
            set_data,
        )
    except Exception as e:
        raise exceptions.MongoDBException(message=str(e))


async def delete_doc(
        data: dict,
        collection: Collection,
) -> None:
    try:
        await collection.delete_one(data)
    except Exception as e:
        raise exceptions.MongoDBException(message=str(e))


async def delete_docs(
        data: dict,
        collection: Collection,
) -> None:
    try:
        await collection.delete_many(data)
    except Exception as e:
        raise exceptions.MongoDBException(message=str(e))
