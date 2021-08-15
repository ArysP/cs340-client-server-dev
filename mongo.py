import csv
import logging
import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient


# Environment variables are read in from an .env file
load_dotenv()
MONGO_USER = os.getenv("MONGO_USER", "Set the username env variable")
MONGO_PASS = os.getenv("MONGO_PASS", "Set the password env variable")
MONGO_HOST = os.getenv("MONGO_HOST", "Set the host env variable")
MONGO_DB = os.getenv("MONGO_DB", "Set the db env variable")


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        self.logger = logging.getLogger(__name__)
        self.username = username
        self.password = password

        # Initialize the MongoClient to access the MongoDB databases and collections.
        uri = "mongodb+srv://{}:{}@{}/{}?authSource=admin".format(
            MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_DB
        )
        self.client = MongoClient(uri)
        self.logger.info("Connected to db")
        self.database = self.client["aac"]
        self.logger.info("Connected to aac.animals")

    def prepare_csv_data(self, csv_file_path):
        # CSV to JSON Conversion
        csv_file = open(csv_file_path, "r")
        csv_reader = csv.DictReader(csv_file)
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
        counter = 0
        for row in csv_reader:
            data: dict = {}
            for field in header:
                data[field] = row[field]
            self.create(data)
            counter += 1
            self.logger.info("Inserted 1 row")
        self.logger.info(f"Inserted {len(counter)} rows.")

    def create(self, data: dict):
        """
        A method that inserts a document into a specified MongoDB database and collection

        :param data: set of key/value pairs in the data type acceptable to the MongoDB driver insert API call
        :return: Returns True if successful insert, else False
        """
        try:
            if data is not None:
                self.database.animals.insert_one(data)  # data should be dictionary
                return True
            else:
                raise Exception("Nothing to save, because data parameter is empty")
        except Exception as e:
            self.logger.exception(
                f"Encountered an exception {e} when trying to save, because data parameter is empty"
            )
            return False

    def read(self, data: dict):
        """
        A method that reads and queries for documents from a specified MongoDB database and collection

        :param data: the key/value lookup pair to use with the MongoDB driver find API call
        :return: result in cursor if successful, else MongoDB returned error message
        """
        try:
            if data is not None:
                return self.database.animals.find(data, {"_id": False})
            else:
                raise Exception("Nothing to read, because data cannot be found")
        except Exception as e:
            self.logger.exception(f"Encountered an exception {e} when trying to read the data")
            return False

    def read_all(self):
        """
        A method that reads all documents from a specified MongoDB database and collection

        :return: result in cursor if successful, else MongoDB returned error message
        """
        try:
            return self.database.animals.find({}, {"_id": False}).limit(10)
        except Exception as e:
            self.logger.exception(f"Encountered an exception {e} when trying to read all the data")
            return False

    def filter_mountain_wilderness(self):
        """
        A method that filters documents for Mountain or Wilderness Rescue dogs with the following criteria:

        Mountain or Wilderness Rescue
            "breed":  "German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"
            "sex_upon_outcome": "Intact Male"
            "age_upon_outcome_in_weeks": gt> 26
            "age_upon_outcome_in_weeks": lt> 156

        :return: result in cursor if successful, else MongoDB returned error message
        """
        try:
            return self.database.animals.find(
                {
                    "breed": {"$regex": "German Shepherd"},
                    "breed": {"$regex": "Alaskan Malamute"},
                    "breed": {"$regex": "Old English Sheepdog"},
                    "breed": {"$regex": "Siberian Husky"},
                    "breed": {"$regex": "Rottweiler"},
                    "sex_upon_outcome": "Intact Male",
                    "age_upon_outcome_in_weeks": {"$gt": "26"},
                    "age_upon_outcome_in_weeks": {"$lt": "156"},
                },
                {"_id": False},
            )
        except Exception as e:
            self.logger.exception(
                f"Encountered an exception {e} when trying to filter to  Mountain or Wilderness Rescue data"
            )
            return False

    def filter_water_rescue(self):
        """
        A method that filters documents for Water Rescue dogs with the following criteria:

        Water Rescue
            "breed": 'Labrador Retriever Mix','Chesapeake Bay Retriever','Newfoundland'
            "sex_upon_outcome": "Intact Female"
            "age_upon_outcome_in_weeks": gt> 26
            "age_upon_outcome_in_weeks": lt> 156

        :return: result in cursor if successful, else MongoDB returned error message
        """
        try:
            return self.database.animals.find(
                {
                    "breed": {"$regex": "Labrador Retriever Mix"},
                    "breed": {"$regex": "Chesapeake Bay Retriever"},
                    "breed": {"$regex": "Newfoundland"},
                    "sex_upon_outcome": "Intact Female",
                    "age_upon_outcome_in_weeks": {"$gt": "26"},
                    "age_upon_outcome_in_weeks": {"$lt": "156"},
                },
                {"_id": False},
            )
        except Exception as e:
            self.logger.exception(
                f"Encountered an exception {e} when trying to filter to  Mountain or Wilderness Rescue data"
            )
            return False

    def filter_disaster_rescue_tracking(self):
        """
        A method that filters documents for Water Rescue dogs with the following criteria:

        Disaster Rescue or Individual Tracking
            "breed":  "Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"
            "sex_upon_outcome": "Intact Male"
            "age_upon_outcome_in_weeks": gt> 26
            "age_upon_outcome_in_weeks": lt> 300

        :return: result in cursor if successful, else MongoDB returned error message
        """
        try:
            return self.database.animals.find(
                {
                    "breed": {"$regex": "Doberman Pinscher"},
                    "breed": {"$regex": "German Shepherd"},
                    "breed": {"$regex": "Golden Retriever"},
                    "breed": {"$regex": "Bloodhound"},
                    "breed": {"$regex": "Rottweiler"},
                    "sex_upon_outcome": "Intact Male",
                    "age_upon_outcome_in_weeks": {"$gt": "26"},
                    "age_upon_outcome_in_weeks": {"$lt": "300"},
                },
                {"_id": False},
            )
        except Exception as e:
            self.logger.exception(
                f"Encountered an exception {e} when trying to filter to  Mountain or Wilderness Rescue data"
            )
            return False

    def update(self, filter: dict, data: dict):
        """
        A method that queries for and changes document(s) from a specified MongoDB database and specified collection

        :param filter: the key/value lookup pair to filter the data
        :param data: the key/value lookup pair to use with the MongoDB driver find API call
        :return: result in JSON format if successful, else MongoDB returned error message.
        """
        try:
            if data is not None:
                self.logger.info(f"Updating id {filter} with new value: {data}")
                return self.database.animals.update_one(filter, data)

            else:
                raise Exception("Nothing to update, because data was not provided")
        except Exception as e:
            self.logger.exception(f"Encountered an exception {e} when trying to update the data")
            return False

    def delete(self, data: dict):
        """
        A method that queries for and removes document(s) from a specified MongoDB database and specified collection

        :param data: the key/value lookup pair to use with the MongoDB driver find API call
        :return: result in JSON format if successful, else MongoDB returned error message.
        """
        try:
            if data is not None:
                print(f"Deleting {data}")
                return self.database.animals.delete_one(data)
            else:
                raise Exception("Nothing to delete, because data was not provided")
        except Exception as e:
            self.logger.exception(f"Encountered an exception {e} when trying to delete the data")
            return False


if __name__ == "__main__":
    aac = AnimalShelter("aac", "pass")
    print(f"Connected to {aac.database.name} Database.")

    # Load the shelter outcomes into the MongoDB
    # file_path = "data/aac_shelter_outcomes.csv"
    # aac.prepare_csv_data(file_path)

    # Query the shelter outcomes for a specific breed
    # dictionary_data = {"breed": "Siamese Mix"}
    # siamese_results = aac.read(dictionary_data)
    # print([result for result in siamese_results][0:5])
    #
    # # Updating a breed of "Domestic Shorthair Mix" from animal_type of 'Cat' to 'cattt'.
    # breed_filter = {"breed": "Domestic Shorthair Mix"}
    #
    # # Values to be updated.
    # new_value = {"$set": {"animal_type": "Cat"}}
    # aac.update(breed_filter, new_value)
    #
    # # Delete example
    # aac.delete({"_id": ObjectId("60fb6aaf2015ac73429bc0c2")})
    results = [r for r in aac.filter_disaster_rescue_tracking()]
    print(f"Number of results: {len(results)}")
    print(results)

    """
    Reset (returns all widgets to their original, unfiltered state)
    """
