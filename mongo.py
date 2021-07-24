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
from collections import OrderedDict

from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import logging
import csv

# Environment variables are read in from an .env file
MONGO_USER = os.getenv("MONGO_USER", "Set the username env variable")
MONGO_PASS = os.getenv("MONGO_PASS", "Set the password env variable")
MONGO_HOST = os.getenv("MONGO_HOST", "Set the host env variable")
MONGO_DB = os.getenv("MONGO_DB", "Set the db env variable")


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Initialize the MongoClient to access the MongoDB databases and collections.
        uri = "mongodb+srv://{}:{}@{}/{}?authSource=admin".format(
            MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_DB
        )
        self.client = MongoClient(uri)
        # self.client = MongoClient(
        #     host="mongodb+srv://cluster0.wdpb3.mongodb.net/",
        #     username=username,
        #     password=password,
        #     # authSource="admin",
        #     authMechanism="SCRAM-SHA-256",
        # )
        self.logger.info("Connected to db")
        self.database = self.client["aac"]
        self.logger.info("Connected to aac.animals")

    def prepare_csv_data(self, file_path):
        # CSV to JSON Conversion
        csv_file = open(file_path, "r")
        csv_reader = csv.DictReader(csv_file)

        db = aac.database
        header = [
            "1",
            "age_upon_outcome",
            "animal_id",
            "animal_type",
            "breed",
            "color",
            "date_of_birth",
            "datetime",
            "monthyear",
            "name",
            "outcome_subtype",
            "outcome_type",
            "sex_upon_outcome",
            "location_lat",
            "location_long",
            "age_upon_outcome_in_weeks",
        ]

        for row in csv_reader:
            data: dict = {}
            for field in header:
                data[field] = row[field]
            self.create(data)
            # self.database.animals.insert_one(data)
            # self.logger.info("Inserted 1 row")
            # print(f"Inserted {data}")

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert_one(data)  # data should be dictionary
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD.


if __name__ == "__main__":
    aac = AnimalShelter()
    # print(aac.client.get_database(name="animals"))
    print(f"Database: {aac.database.name}")

    file_path = "data/aac_shelter_outcomes.csv"
    aac.prepare_csv_data(file_path)

    # with open(file_path, "r") as read_obj:
    #     # pass the file object to reader() to get the reader object
    #     csv_reader = csv.DictReader(read_obj)
    #     # Pass reader object to list() to get a list of lists
    #     mylist = list(csv_reader)
    #     # print(list_of_rows)
    #     x = animals.insert_many(mylist)
    #
    #     # print list of the _id values of the inserted documents:
    #     print(x.inserted_ids)
