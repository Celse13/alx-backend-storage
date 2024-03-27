#!/usr/bin/env python3
""" Redis cache """


import redis
import uuid


class Cache:
    def __init__(self):
        """ init func """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
