from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDB:
    def __init__(self, db_name, collection_name,
                 uri="mongodb+srv://Aditya:Aditya@acr-user-data.3el6t.mongodb.net/?retryWrites=true&w=majority&appName=ACR-user-data"):
        """
        Initialize connection to MongoDB (local or cloud).
        :param db_name: Name of the database
        :param collection_name: Name of the collection
        :param uri: MongoDB connection URI (default is local MongoDB)
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"Connected to MongoDB | Database: {db_name} | Collection: {collection_name}")
        except ConnectionFailure as e:
            print("Error: Unable to connect to MongoDB", e)

    ## ---------------- CREATE OPERATIONS ---------------- ##
    def insert_one(self, data):
        """ Insert a single document. """
        result = self.collection.insert_one(data)
        return result.inserted_id

    def insert_many(self, data_list):
        """ Insert multiple documents. """
        result = self.collection.insert_many(data_list)
        return result.inserted_ids

    ## ---------------- READ OPERATIONS ---------------- ##
    def find_one(self, query):
        """ Find a single document that matches the query. """
        return self.collection.find_one(query)

    def find_all(self, query={}, limit=0):
        """ Find all documents that match the query. Use limit to restrict results. """
        return list(self.collection.find(query).limit(limit))

    def find_with_projection(self, query={}, projection=None):
        """ Find documents with selected fields. """
        return list(self.collection.find(query, projection))

    ## ---------------- UPDATE OPERATIONS ---------------- ##
    def update_one(self, query, update_values):
        """ Update a single document. """
        result = self.collection.update_one(query, {"$set": update_values})
        return result.modified_count

    def update_many(self, query, update_values):
        """ Update multiple documents. """
        result = self.collection.update_many(query, {"$set": update_values})
        return result.modified_count

    ## ---------------- DELETE OPERATIONS ---------------- ##
    def delete_one(self, query):
        """ Delete a single document. """
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many(self, query):
        """ Delete multiple documents. """
        result = self.collection.delete_many(query)
        return result.deleted_count

    ## ---------------- ADVANCED FEATURES ---------------- ##
    def create_index(self, field_name, order=1):
        """ Create an index on a field (1 for ascending, -1 for descending). """
        return self.collection.create_index([(field_name, order)])

    def aggregate(self, pipeline):
        """ Perform an aggregation query. """
        return list(self.collection.aggregate(pipeline))

    def count_documents(self, query=dict()):
        """ Count documents matching the query. """
        return self.collection.count_documents(query)

    def drop_collection(self):
        """ Drop the entire collection. """
        self.collection.drop()
        print("Collection dropped successfully.")

    ## ---------------- CONNECTION MANAGEMENT ---------------- ##
    def close_connection(self):
        """ Close the MongoDB connection. """
        self.client.close()
        print("MongoDB connection closed.")

