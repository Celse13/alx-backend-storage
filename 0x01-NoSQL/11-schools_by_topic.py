#!/usr/bin/env python3
""" Return documents """


def schools_by_topic(mongo_collection, topic):
    """ return documents """
    return mongo_collection.find({"topics": topic}
