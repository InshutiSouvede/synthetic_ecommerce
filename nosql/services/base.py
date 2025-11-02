"""Base service class and utilities for all services"""

def convert_objectid_to_string(document):
    """Convert ObjectId to string in a document"""
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    return document