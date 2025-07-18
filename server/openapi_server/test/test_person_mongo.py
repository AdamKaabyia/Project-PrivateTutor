import unittest
from datetime import datetime
from bson import ObjectId

from server.openapi_server.models.DB_utils import (
    save_person_to_mongo,
    get_person_from_mongo,
    update_person_in_mongo,
    delete_person_from_mongo,
    mongo_db
)
from server.openapi_server.models.person import Person


class TestPersonDbOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection_name = "test_persons"
        cls.collection = mongo_db.get_collection(cls.collection_name)

        # Create a test person instance
        cls.test_person = Person(
            id=None,  # MongoDB will generate the `_id`
            name="John Doe",
            phone="1234567890",
            email="johndoe@example.com",
            about_section="Test about section",
            available=[datetime.now()],
            rating=4.5
        )

        # Save the test person to the database
        result = save_person_to_mongo(cls.collection_name, cls.test_person)
        if not result["acknowledged"]:
            raise RuntimeError("Failed to save test person to MongoDB.")

        cls.inserted_id = result.get("inserted_id")
        if not cls.inserted_id:
            raise RuntimeError("Inserted ID is None. Check save_person_to_mongo.")

    def test_save_person(self):
        # Save the test person
        save_result = save_person_to_mongo(self.collection_name, self.test_person)
        self.assertTrue(save_result["acknowledged"], "Save was not acknowledged.")
        self.assertIsNotNone(save_result.get("inserted_id"), "No ID was returned for the saved person.")

    def test_get_person(self):
        # Ensure inserted_id is valid
        self.assertIsNotNone(self.inserted_id, "Inserted ID is None. Setup failed.")

        # Retrieve the person using its ID
        retrieved_person = get_person_from_mongo(self.collection_name, self.inserted_id)
        self.assertIsNotNone(retrieved_person, "Person not found.")
        self.assertEqual(retrieved_person.name, self.test_person.name, "Name does not match.")
        self.assertEqual(retrieved_person.email, self.test_person.email, "Email does not match.")

    def test_update_person(self):
        # Update the person's phone number
        updated_phone = "0987654321"
        update_result = update_person_in_mongo(self.collection_name, str(self.inserted_id), {"phone": updated_phone})
        self.assertTrue(update_result["acknowledged"], "Update was not acknowledged.")
        self.assertGreater(update_result["modified_count"], 0, "No documents were modified.")

        # Verify the update
        updated_person = get_person_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertIsNotNone(updated_person, "Person not found after update.")
        self.assertEqual(updated_person.phone, updated_phone, "Updated phone does not match.")

    def test_delete_person(self):
        # Save and then delete the test person
        save_result = save_person_to_mongo(self.collection_name, self.test_person)
        delete_result = delete_person_from_mongo(self.collection_name, str(save_result.get("inserted_id")))
        self.assertTrue(delete_result["acknowledged"], "Delete was not acknowledged.")
        self.assertEqual(delete_result["deleted_count"], 1, "No documents were deleted.")

        # Verify deletion
        deleted_person = get_person_from_mongo(self.collection_name, str(save_result.get("inserted_id")))
        self.assertIsNone(deleted_person, "Person was not deleted.")


if __name__ == '__main__':
    unittest.main()
