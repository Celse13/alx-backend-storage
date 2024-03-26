#!/usr/bin/env python3
""" Log stats """


from pymongo import MongoClient


def log_stats():
    """ logs """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(f"{logs_collection.count_documents({})} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {logs_collection.count_documents({'method': method})}")
    print(f"{logs_collection.count_documents({'method': 'GET', 'path': '/status'})} status check")


if __name__ == "__main__":
    log_stats()
