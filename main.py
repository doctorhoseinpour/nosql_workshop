from fastapi import FastAPI
import uvicorn
import random
import string
from mongo_app.database import MongoDatabase
from mongo_app import crud
from exceptions import handlers
from datetime import datetime
from pymongo.results import InsertOneResult
import asyncio
import redis
import time

app = FastAPI()


async def generate_data():
    mongo_db = MongoDatabase(
        database_url='mongodb://localhost:27017',
        database_name='test',
    )

    for i in range(100):
        await crud.create_doc(
            data={
                'name': ''.join(random.choices(string.ascii_lowercase, k=10)),
                'score': random.randint(1, 100),
                'graduated': True if random.randint(1, 100) < 50 else False,
                'units': random.randint(1, 140)
            },
            collection=mongo_db.student_collection
        )

    workspace: InsertOneResult = await crud.create_doc(
        data={
            'owner': 'alireza',
            'name': 'workspace 1',
            'created_at': datetime.now()
        },
        collection=mongo_db.work_space_collection
    )

    await crud.create_doc(
        data={
            'workspace_id': workspace.inserted_id,
            'name': 'creative 1',
            'width': 100,
            'height': 100,
            'created_at': datetime.now(),
            'widgets': [
                {
                    'type': 'square',
                    'x': 30,
                    'y': 50
                },
                {
                    'type': 'circle',
                    'r': 40,
                }
            ]
        },
        collection=mongo_db.creative_collection
    )

    await crud.create_doc(
        data={
            'workspace_id': workspace.inserted_id,
            'name': 'creative 2',
            'width': 100,
            'height': 100,
            'created_at': datetime.now(),
            'widgets': [
                {
                    'type': 'square',
                    'x': 200,
                    'y': 200
                },
                {
                    'type': 'circle',
                    'r': 40,
                }
            ]
        },
        collection=mongo_db.creative_collection
    )


async def delete_data():
    mongo_db = MongoDatabase(
        database_url='mongodb://localhost:27017',
        database_name='test',
    )

    await crud.delete_docs(
        data={
            'score': {'$lt': 50}
        },
        collection=mongo_db.student_collection
    )

    await crud.delete_docs(
        data={
            'widgets.x': {'$lt': 100}
        },
        collection=mongo_db.creative_collection
    )


async def update_data():
    mongo_db = MongoDatabase(
        database_url='mongodb://localhost:27017',
        database_name='test',
    )

    await crud.update_doc(
        query_data={
            'name': 'creative 2'
        },
        set_data={
            '$set': {
                'height': 1000,
                'width': 1000,
                'widgets': []
            }
        },
        collection=mongo_db.creative_collection
    )


def redis_check():
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

    print(redis_db.keys())
    redis_db.set('ali', 'reza')

    # EX seconds -- Set the specified expire time, in seconds.
    # PX milliseconds -- Set the specified expire time, in milliseconds.
    # EXAT timestamp-seconds -- Set the specified Unix time at which the key will expire, in seconds.
    # PXAT timestamp-milliseconds -- Set the specified Unix time at which the key will expire, in milliseconds.
    # NX -- Only set the key if it does not already exist.
    # XX -- Only set the key if it already exists.
    # KEEPTTL -- Retain the time to live associated with the key.
    # GET -- Return the old string stored at key, or nil if key did not exist. An error is returned and SET aborted if the value stored at key is not a string.

    print(redis_db.keys())

    redis_db.set('5555', '12', ex=5)
    print(redis_db.get('5555'))
    time.sleep(6)
    print('5555 value: ', redis_db.get('5555'))

    redis_db.hset('1234', '1', 'reza')
    redis_db.hset('1234', '2', 'ali')
    redis_db.hset('1234', '3', 'hamid')
    redis_db.hset('1234', '312312', 'majid')

    print(redis_db.hgetall('1234'))

    print(redis_db.keys())

    redis_db.delete('1234')

    print(redis_db.keys())

    print(redis_db.get('twilio'))
    redis_db.incr('twilio', 5)
    print(redis_db.get('twilio'))

    redis_db.lpush('my-list', 5, 7, 12, 19, 31, 13, 23)
    print(redis_db.lrange('my-list', 0, -1))

    redis_db.lpop(name='my-list')
    print(redis_db.lrange('my-list', 0, -1))

    redis_db.ltrim('my-list', 1, 3)
    print(redis_db.lrange('my-list', 0, -1))

    redis_db.lrem('my-list', 1, 31)
    print(redis_db.lrange('my-list', 0, -1))

    for i in range(0, redis_db.llen('my-list')):
        value = int(redis_db.lindex('my-list', i)) * 2
        redis_db.lset('my-list', i, f'{value}')
    print(redis_db.lrange('my-list', 0, -1))

    redis_db.flushdb()


def main():
    # asyncio.run(generate_data())
    # asyncio.run(delete_data())
    # asyncio.run(update_data())
    redis_check()


if __name__ == "__main__":
    main()
