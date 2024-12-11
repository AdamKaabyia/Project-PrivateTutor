import unittest
from datetime import datetime
from bson import ObjectId

from server.openapi_server.models.DB_utils import (
    save_meeting_to_mongo,
    get_meeting_from_mongo,
    update_meeting_in_mongo,
    delete_meeting_from_mongo,
    mongo_db
)
from server.openapi_server.models.meeting import Meeting


class TestMeetingDbOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection_name = "test_meetings"
        cls.collection = mongo_db.get_collection(cls.collection_name)

        # Create a test meeting instance
        cls.test_meeting = Meeting(
            location="Test Location",
            start_time=datetime.now(),
            finish_time=datetime.now(),
            subject="Test Subject",
            people=[],
            attached_files=[]
        )

        # Save the test meeting to the database
        result = save_meeting_to_mongo(cls.collection_name, cls.test_meeting)
        if not result["acknowledged"]:
            raise RuntimeError("Failed to save test meeting to MongoDB.")

        cls.inserted_id = result["inserted_id"]

    # @classmethod
    # def tearDownClass(cls):
    #     # Clean up by deleting the test meeting from the database
    #     delete_meeting_from_mongo(cls.collection_name, str(cls.inserted_id))

    def test_save_meeting(self):
        # Verify that the meeting was saved successfully
        meeting = self.collection.find_one({"_id": ObjectId(self.inserted_id)})
        self.assertIsNotNone(meeting, "Meeting was not saved to MongoDB.")
        self.assertEqual(meeting["location"], self.test_meeting.location, "Saved location does not match.")

    def test_get_meeting(self):
        # Retrieve the meeting using its ID
        retrieved_meeting = get_meeting_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertIsInstance(retrieved_meeting, Meeting, "Retrieved object is not a Meeting instance.")
        self.assertEqual(retrieved_meeting.location, self.test_meeting.location, "Location does not match.")
        self.assertEqual(retrieved_meeting.subject, self.test_meeting.subject, "Subject does not match.")

    def test_update_meeting(self):
        # Update the meeting location
        updated_location = "Updated Location"
        update_result = update_meeting_in_mongo(self.collection_name, str(self.inserted_id), {"location": updated_location})
        self.assertTrue(update_result["acknowledged"], "Update was not acknowledged.")
        self.assertGreater(update_result["modified_count"], 0, "No documents were modified.")

        # Verify the update
        updated_meeting = get_meeting_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertEqual(updated_meeting.location, updated_location, "Updated location does not match.")

    def test_delete_meeting(self):
        # Delete the meeting
        delete_result = delete_meeting_from_mongo(self.collection_name, str(self.inserted_id))
        self.assertTrue(delete_result["acknowledged"], "Delete was not acknowledged.")
        self.assertEqual(delete_result["deleted_count"], 1, "No documents were deleted.")

        # Verify deletion
        with self.assertRaises(ValueError):
            get_meeting_from_mongo(self.collection_name, str(self.inserted_id))


if __name__ == '__main__':
    unittest.main()