import unittest
from datetime import datetime
from bson import ObjectId  # Ensure this is imported to handle MongoDB ObjectIds
from server.openapi_server.models.File import File
from server.openapi_server.models.DB_utils import save_file_to_mongo, load_file_from_mongo, mongo_db


class TestFileMongoOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use the existing global MongoDatabase instance
        cls.collection_name = "pydantic"
        cls.collection = mongo_db.get_collection(cls.collection_name)

        # Create and insert the file object
        cls.test_file = File(
            file_name="fianl_test.txt",
            file_type="text/plain",
            file_content=b"Hello, world!",
            owner_id=3222221111,
            upload_date=datetime.now()
        )
        # Save the file to MongoDB
        try:
            result = save_file_to_mongo(cls.collection_name, cls.test_file)
            if not result["acknowledged"]:
                raise RuntimeError("MongoDB operation was not acknowledged.")
            cls.inserted_id = result["inserted_id"]
        except Exception as e:
            raise RuntimeError(f"Failed to save file to MongoDB: {e}")

    @classmethod
    def tearDownClass(cls):
        # Cleanup: Remove the inserted file
        if hasattr(cls, 'inserted_id') and cls.inserted_id:
            cls.collection.delete_one({'_id': cls.inserted_id})

    def test_store_and_extract_file(self):
        # Extract the file using its ID and validate
        try:
            extracted_file = load_file_from_mongo(self.collection_name, self.inserted_id)

            # Check that the extracted file matches the one we saved
            self.assertEqual(extracted_file.file_name, self.test_file.file_name)
            self.assertEqual(extracted_file.file_type, self.test_file.file_type)
            self.assertEqual(extracted_file.file_content, self.test_file.file_content)
            self.assertEqual(extracted_file.owner_id, self.test_file.owner_id)
            # Compare dates in a formatted string since direct datetime comparison might fail due to precision issues in serialization
            self.assertEqual(
                extracted_file.upload_date.strftime("%Y-%m-%d %H:%M:%S"),
                self.test_file.upload_date.strftime("%Y-%m-%d %H:%M:%S")
            )
        except RuntimeError as e:
            self.fail(f"Error during test execution: {e}")


if __name__ == '__main__':
    unittest.main()
