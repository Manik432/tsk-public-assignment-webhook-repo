import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
import time
from datetime import datetime, timezone

last_fetch_id = None

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def post_action_to_database(new_action):
    global db

    client = db.client

    database = client['GithubActions']
    action_schema_collection = database['ActionSchema']
   #  document_list = [{ "name" : "Abcd's Burgers" }]
    document_list = [new_action.to_document()]

    inserted_documents = action_schema_collection.insert_many(document_list)

def get_latests_actions_from_database():
    global db
    global last_fetch_id
    client = db.client

    database = client['GithubActions']
    action_schema_collection = database['ActionSchema']

    query_filter = {
    '_id': {
        '$gt': last_fetch_id,
    }
}
    if last_fetch_id == None:
         documents = action_schema_collection.find()
    else:
        documents = action_schema_collection.find(query_filter)

    documents = list(documents)

    for document in documents:
         utctime = document.get('timestamp')
         day_with_suffix = get_day_with_suffix(utctime.day)
         formatted_timestamp = utctime.strftime(f"{day_with_suffix} %B %Y - %I:%M %p UTC")
         document['timestamp'] = formatted_timestamp
         last_fetch_id = document['_id']

    return documents

def get_day_with_suffix(day):
        if 11 <= day <= 13:
            return f"{day}th"
        else:
            suffixes = {1: "st", 2: "nd", 3: "rd"}
            return f"{day}{suffixes.get(day % 10, 'th')}"
