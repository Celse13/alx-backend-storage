#!/usr/bin/env python3
import requests
import redis
from functools import wraps
""" Caching """


r = redis.Redis()


def cache_page(func):
    """Decorator to cache web pages and track access count."""
    @wraps(func)
    def wrapper(url):
        if r.get(url):
            r.incr(f"count:{url}")
            return r.get(url).decode('utf-8')
        else:
            page = func(url)
            r.setex(url, 10, page)
            r.incr(f"count:{url}")
            return page
    return wrapper

@cache_page
def get_page(url: str) -> str:
    """Fetch a web page."""
    response = requests.get(url)
    return response.text
