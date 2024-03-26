#!/usr/bin/env python3
""" Insert the school """


def insert_school(mongo_collection, **kwargs):
    """ Insert document """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
