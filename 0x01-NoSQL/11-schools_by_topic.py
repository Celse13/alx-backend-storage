#!/usr/bin/env python3
""" all documents """


def schools_by_topic(mongo_collection, topic):
    """ all documents """
    return mongo_collection.find({"topics": topic})
