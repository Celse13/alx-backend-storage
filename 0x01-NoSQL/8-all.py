#!/usr/bin/env python3
""" List all document """


def list_all(mongo_collection):
    documents = mongo_collection.find()
    return list(documents)