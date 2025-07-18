import unittest
from datetime import datetime
from server.openapi_server.models.DB_utils import *
from server.openapi_server.models.meeting import Meeting


class TestMeetingDbOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection_name = "pydantic test_meetings"
        cls.collection = mongo_db.get_collection(cls.collection_name)

    def setUp(self):
        # Create a fresh test meeting instance for each test
        self.test_meeting = Meeting(
            location="Test Location",
            start_time=datetime.now(),
            finish_time=datetime.now(),
            subject="testing meeting mongo final",
            people=[],
            attached_files=[]
        )

        # Save the test meeting to the database
        result = save_meeting_to_mongo(self.collection_name, self.test_meeting)
        if not result["acknowledged"]:
            raise RuntimeError("Failed to save test meeting to MongoDB.")

        self.inserted_id = result.get("inserted_id")
        self.assertIsNotNone(self.inserted_id, "Inserted ID is None after saving meeting.")

    def tearDown(self):
        # Clean up by deleting the test meeting
        delete_meeting_from_mongo(self.collection_name, str(self.inserted_id))

    def test_get_meeting(self):
        # Retrieve the meeting using its ID
        retrieved_meeting = get_meeting_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertIsNotNone(retrieved_meeting, "Meeting not found.")
        self.assertEqual(retrieved_meeting.location, self.test_meeting.location, "Location does not match.")
        self.assertEqual(retrieved_meeting.subject, self.test_meeting.subject, "Subject does not match.")

    def test_save_meeting(self):
        # Verify that the meeting was saved successfully
        meeting = self.collection.find_one({"_id": ObjectId(self.inserted_id)})
        self.assertIsNotNone(meeting, "Meeting was not saved to MongoDB.")
        self.assertEqual(meeting["location"], self.test_meeting.location, "Saved location does not match.")

    def test_update_meeting(self):
        # Update the meeting location
        updated_location = "Updated Location"
        update_result = update_meeting_in_mongo(self.collection_name, str(self.inserted_id), {"location": updated_location})
        self.assertTrue(update_result["acknowledged"], "Update was not acknowledged.")
        self.assertGreater(update_result["modified_count"], 0, "No documents were modified.")

        # Verify the update
        updated_meeting = get_meeting_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertIsNotNone(updated_meeting, "Meeting not found after update.")
        self.assertEqual(updated_meeting.location, updated_location, "Updated location does not match.")

    def test_delete_meeting(self):
        # Delete the meeting
        delete_result = delete_meeting_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertTrue(delete_result["acknowledged"], "Delete was not acknowledged.")
        self.assertEqual(delete_result["deleted_count"], 1, "No documents were deleted.")

        # Verify deletion
        deleted_meeting = get_meeting_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertIsNone(deleted_meeting, "Meeting was not deleted.")

    def test_get_non_existent_meeting(self):
        # Attempt to retrieve a non-existent meeting
        invalid_id = str(ObjectId())  # Generate a random ObjectId
        meeting = get_meeting_from_mongo(self.collection_name, invalid_id)
        self.assertIsNone(meeting, "Non-existent meeting should return None.")

    def test_delete_non_existent_meeting(self):
        # Attempt to delete a non-existent meeting
        invalid_id = str(ObjectId())  # Generate a random ObjectId
        delete_result = delete_meeting_from_mongo(self.collection_name, invalid_id)
        self.assertTrue(delete_result["acknowledged"], "Delete was not acknowledged.")
        self.assertEqual(delete_result["deleted_count"], 0, "Deleted count should be 0 for non-existent meeting.")


if __name__ == '__main__':
    unittest.main()
