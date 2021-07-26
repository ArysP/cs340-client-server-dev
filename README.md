# README cs340-client-server-dev
Repository to store Python and MongoDB code for Client/Server Development

## About the Project
This project aims to fulfill the basic database CRUD operations by executing the following objectives through four functions:
1. a method that **inserts** a document into a specified MongoDB database (`create`)
2. a method that **queries** for documents from a specified MongoDB database and specified collection (`read`)
3. a method that **updates** a document into a specified MongoDB database and specified collection (`update`)
4. a method that **deletes** a document from a specified MongoDB database and specified collection (`delete`)
5. applies industry standard best practices such as naming conventions, exception handling, and in-line comments

This project utilizes the Austin Animal Center Outcomes dataset, which is a sample data set (CSV file) of animal center outcomes. This data set has been modified for the purposes of this project. Specifically, the following columns have been added: location_lat (latitude), location_long (longitude), and age_upon_outcome_in_weeks (the age of the animal, given in weeks).

## Motivation
The motivation behind the creation and maintenance of the project is to create a Python module that enables create, read, update, and delete functionality on a MongoDB.

## Getting Started
To set up the project locally, follow the steps outlined in **Installation** and **Environment Variables** section.

### Installation
- In PyCharm, create a Virtual Environment by navigating to `Settings` > `Projects` > `Project Interpreter` > Clicking the `Cog` icon in the top right > Click "`Add`" > Ensure the new `venv` box is checked > Click "`OK`" > Click "`OK`" again
- Install the requirements file by typing `pip install -r requirements.txt` in the terminal.
- Pymongo has some additional dependencies which can be installed with the following command: `python -m pip install pymongo[snappy,gssapi,srv,tls]`

### Environment Variables
Create a `.env` file in the root of this repo and fill in the following environment variables. This is for example only. Change these variables to what the cluster host IP, post, db, username, and password should be.

```dotenv
MONGO_HOST = "cluster"
MONGO_PORT = "###"
MONGO_DB = "aac"
MONGO_USER = "user"
MONGO_PASS = "pass"
```

## Usage
To run the code locally, follow the **Getting Started** steps and then run `mongo.py`. The Python driver used for interacting with MongoDB was the PyMongo driver package. It was selected because it is the official MongoDB Python driver for MongoDB. It is a frequently used and a well-documented python package with a lot of examples online for debugging. PyMongo was chosen because this driver is continually being maintained and updated by open-source developers and offers concise, clear database functionality.


## Code Example
Run `mongo.py` to connect to the database, create, read, update, and delete a document.

```python
from bson import ObjectId
from mongo import AnimalShelter

# Connect to the database.
# The database connection call requires setting up the environment variables for connecting to the db.
aac = AnimalShelter()

# Load the shelter outcomes into the MongoDB
file_path = "data/aac_shelter_outcomes.csv"
aac.prepare_csv_data(file_path)

# Create one document. 
data = {'_id': ObjectId('60fb736621724ef7c4f9629c'), 
        '1': '4', 
        'age_upon_outcome': '7 months', 
        'animal_id': 'A733653', 
        'animal_type': 'Cat', 
        'breed': 'Siamese Mix', 
        'color': 'Seal Point', 
        'date_of_birth': '2016-01-25', 
        'datetime': '2016-08-27 18:11:00', 
        'monthyear': '2016-08-27T18:11:00', 
        'name': 'Kitty', 'outcome_subtype': '', 
        'outcome_type': 'Adoption', 
        'sex_upon_outcome': 'Intact Female', 
        'location_lat': '30.3188063374257', 
        'location_long': '-97.7240376703891', 
        'age_upon_outcome_in_weeks': '30.8225198412698'}
# The create method takes one argument: data in the form of a dictionary
aac.create(data)

# Read/query the shelter outcomes for a specific breed
# The Read function takes one argument: data in the form of a dictionary. The key:value pairs represent the column and text to find in the database
siamese_results = aac.read({"breed": "Siamese Mix"})
print([result for result in siamese_results][0:5])

# Update the results 'Cattt' (using the breed filter)
'''
The Update function takes two arguments: 
1.	the filter dictionary which contains the key:value to filter on
2.	the data dictionary (which is nested in an outer dictionary with the ‘$set’ key) which contains the key:value pair nested inner-most to find and update find in the database
'''
breed_filter = {"breed": "Domestic Shorthair Mix"}
new_value = {"$set": {"animal_type": "Cattt"}}
aac.update(breed_filter, new_value)

# Delete the duplicate document by _id. This function takes one argument: data in the form of a dictionary (key:value)
aac.delete({"_id": ObjectId("60fb6af04359d8156b7d48d4")})
```

## Tests
Unit tests have not yet been implemented in this project.

## Contact
Arys Pena

## References
Austin Animal Center. (2020). Austin animal center outcomes [Data set]. City of Austin, Texas Open Data Portal. https://doi.org/10.26000/025.000001