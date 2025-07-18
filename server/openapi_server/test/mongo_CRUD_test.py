import unittest
from pymongo.errors import ConnectionFailure

from server.openapi_server.models.Mongo import MongoDatabase


class TestMongoDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize MongoDB connection for testing."""
        try:
            cls.db_instance = MongoDatabase()  # Initialize the MongoDatabase class
            cls.collection_name = "test_collection"
            cls.collection = cls.db_instance.get_collection(cls.collection_name)
            print("Connected to MongoDB successfully.")
        except ConnectionFailure as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")

    def test_insert_and_retrieve(self):
        """Test inserting and retrieving a document."""
        test_document = {"name": "John Doe", "age": 30}

        # Insert the document
        insert_result = self.collection.insert_one(test_document)
        self.assertTrue(insert_result.acknowledged, "Insert operation failed.")

        # Retrieve the document
        retrieved_doc = self.collection.find_one({"_id": insert_result.inserted_id})
        self.assertIsNotNone(retrieved_doc, "Failed to retrieve the inserted document.")
        self.assertEqual(retrieved_doc["name"], "John Doe", "Retrieved name does not match.")
        self.assertEqual(retrieved_doc["age"], 30, "Retrieved age does not match.")

    def test_update_document(self):
        """Test updating a document."""
        # Insert a document
        test_document = {"name": "Jane Doe", "age": 25}
        insert_result = self.collection.insert_one(test_document)
        self.assertTrue(insert_result.acknowledged, "Insert operation failed.")

        # Update the document
        update_result = self.collection.update_one(
            {"_id": insert_result.inserted_id}, {"$set": {"age": 26}}
        )
        self.assertEqual(update_result.modified_count, 1, "Update operation failed.")

        # Verify the update
        updated_doc = self.collection.find_one({"_id": insert_result.inserted_id})
        self.assertEqual(updated_doc["age"], 26, "Updated age does not match.")

    def test_delete_document(self):
        """Test deleting a document."""
        # Insert a document
        test_document = {"name": "Mark Smith", "age": 40}
        insert_result = self.collection.insert_one(test_document)
        self.assertTrue(insert_result.acknowledged, "Insert operation failed.")

        # Delete the document
        delete_result = self.collection.delete_one({"_id": insert_result.inserted_id})
        self.assertEqual(delete_result.deleted_count, 1, "Delete operation failed.")

        # Verify deletion
        deleted_doc = self.collection.find_one({"_id": insert_result.inserted_id})
        self.assertIsNone(deleted_doc, "Document still exists after deletion.")

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        try:
            cls.collection.drop()  # Drop the test collection
            print(f"Cleaned up test collection '{cls.collection_name}'.")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")


if __name__ == "__main__":
    unittest.main()
