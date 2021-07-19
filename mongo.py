"""
Develop a CRUD class that, when instantiated, provides the following functionality:

A method that inserts a document into a specified MongoDB database and collection
- Input -> argument to function will be set of key/value pairs in the data type acceptable to the MongoDB driver insert API call
- Return -> “True” if successful insert, else “False”

A method that queries for documents from a specified MongoDB database and specified collection
- Input -> arguments to function should be the key/value lookup pair to use with the MongoDB driver find API call
- Return -> result in cursor if successful, else MongoDB returned error message

Important: Be sure to use find() instead of find_one() when developing your method.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import os


# Environment variables are read in from an .env file
username = os.getenv('USERNAME', "Set the username env variable")
password = os.getenv('PASSWORD', "Set the password env variable")
port = os.getenv('PORT')


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        # "mongodb+srv://cluster0.wdpb3.mongodb.net/aac"
        self.client = MongoClient(f'mongodb://%{username}:%{password}@localhost:{port}')
        self.database = self.client['project']

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert(data)  # data should be dictionary
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD.


if __name__ == '__main__':
    shelter = AnimalShelter()
    print(shelter)
    # shelter.create()