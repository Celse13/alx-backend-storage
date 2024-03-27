#!/usr/bin/env python3
"""Module documentation"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(func: Callable) -> Callable:
    """Decorator to count function calls"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wrapped function"""
        func_key = func.__qualname__
        self._redis.incr(func_key)
        return func(self, *args, **kwargs)

    return wrapper

def call_history(func: Callable) -> Callable:
    """Decorator to track function calls"""
    input_key = func.__qualname__ + ":inputs"
    output_key = func.__qualname__ + ":outputs"

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wrapped function"""
        self._redis.rpush(input_key, str(args))
        result = func(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper

def replay(func: Callable) -> None:
    """Function to display function calls"""
    input_key = "{}:inputs".format(func.__qualname__)
    output_key = "{}:outputs".format(func.__qualname__)

    inputs = func.__self__._redis.lrange(input_key, 0, -1)
    outputs = func.__self__._redis.lrange(output_key, 0, -1)

    print("{} was invoked {} times:".format(func.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                func.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )

class Cache:
    """Class documentation"""

    def __init__(self):
        """Initialization method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method to save data"""
        unique_key = str(uuid.uuid4())
        self._redis.set(unique_key, data)
        return unique_key

    def get(
        self, key_str: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """Method to retrieve data"""
        retrieved_value = self._redis.get(key_str)
        if fn:
            retrieved_value = fn(retrieved_value)
        return retrieved_value

    def get_str(self, key_str: str) -> str:
        """Method to retrieve string data"""
        return self.get(key_str, fn=str)

    def get_int(self, key_str: str) -> int:
        """Method to retrieve integer data"""
        return self.get(key_str, fn=int)
