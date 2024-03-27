#!/usr/bin/env python3
""" Redis documentation """


import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count_calls class"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        k = method.__qualname__
        self._redis.incr(k)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ history class"""
    inner_k = method.__qualname__ + ":inputs"
    outer_K = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        self._redis.rpush(inner_k, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outer_K, str(output))
        return output

    return wrapper


def replay(method: Callable) -> None:
    """doc doc class"""
    inside_key = "{}:inputs".format(method.__qualname__)
    outside_key = "{}:outputs".format(method.__qualname__)

    opts = method.__self__._redis.lrange(inside_key, 0, -1)
    inpts = method.__self__._redis.lrange(outside_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(opts)))
    for incom, out in zip(opts, inpts):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, incom.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """Cache class"""

    def __init__(self):
        """ constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store class"""
        k = str(uuid.uuid4())
        self._redis.set(k, data)
        return k

    def get(
        self, key_str: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """get class"""
        retrieved_value = self._redis.get(key_str)
        if fn:
            retrieved_value = fn(retrieved_value)
        return retrieved_value

    def get_str(self, key_str: str) -> str:
        """get string class"""
        return self.get(key_str, fn=str)

    def get_int(self, key_str: str) -> int:
        """get int class"""
        return self.get(key_str, fn=int)
