#!/usr/bin/env python3
""" Show list of students """


def top_students(mongo_collection):
    """ students list """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
