import motor.motor_asyncio
import pymongo
from pymongo.collection import Collection


class MongoDatabase:
    def __init__(self, database_url: str, database_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(database_url)
        self.mongo_database = self.client[database_name]
        self.work_space_collection:\
            Collection =\
            self.mongo_database.get_collection("work_space_collection")
        self.creative_collection:\
            Collection =\
            self.mongo_database.get_collection("creative_collection")

        self.student_collection: \
            Collection = \
            self.mongo_database.get_collection("student")
        # CREATIVE INDEX
        self.creative_collection.create_index(
            [
                ("work_space_id", pymongo.DESCENDING),
                ("name", pymongo.DESCENDING),
            ],
            unique=True,
        )
        self.creative_collection.create_index(
            [
                ("created_at", pymongo.DESCENDING),
            ],
        )
