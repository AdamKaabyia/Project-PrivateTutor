import unittest
from datetime import datetime
from bson import ObjectId

from server.openapi_server.models.DB_utils import (
    save_teacher_to_mongo,
    get_teacher_from_mongo,
    update_teacher_in_mongo,
    delete_teacher_from_mongo,
    mongo_db
)
from server.openapi_server.models.teacher import Teacher


class TestTeacherDbOperations(unittest.TestCase):
    def setUp(self):
        self.collection_name = "test_teachers"
        self.collection = mongo_db.get_collection(self.collection_name)

        # Create a test teacher instance
        self.test_teacher = Teacher(
            id=str(ObjectId()),
            name="Mr. Smith",
            phone="1234567890",
            email="mrsmith@example.com",
            about_section="Experienced history teacher",
            available=[datetime.now()],
            rating=4.9,
            subjects_to_teach=["History", "Geography"],
            hourly_rate=50.0,
            meetings=[{
                "location": "Classroom",
                "start_time": datetime.now().isoformat(),
                "finish_time": datetime.now().isoformat(),
                "subject": "History",
                "people": [],
                "attached_files": []
            }]
        )

        # Save the test teacher to the database
        result = save_teacher_to_mongo(self.collection_name, self.test_teacher)
        if not result.get("inserted_id"):
            raise RuntimeError("Failed to save test teacher to MongoDB.")
        self.inserted_id = result["inserted_id"]

    def tearDown(self):
        # Clean up test data
        self.collection.delete_many({})

    def test_save_teacher(self):
        # Verify that the teacher was saved successfully
        teacher = self.collection.find_one({"_id": ObjectId(self.inserted_id)})
        self.assertIsNotNone(teacher, "Teacher was not saved to MongoDB.")
        self.assertEqual(teacher["name"], self.test_teacher.name, "Saved name does not match.")

    def test_get_teacher(self):
        # Retrieve the teacher using its ID
        retrieved_teacher = get_teacher_from_mongo(self.collection_name, self.inserted_id)
        self.assertIsNotNone(retrieved_teacher, "Teacher not found.")
        self.assertEqual(retrieved_teacher.name, self.test_teacher.name, "Name does not match.")
        self.assertEqual(retrieved_teacher.email, self.test_teacher.email, "Email does not match.")

    def test_update_teacher(self):
        # Update the teacher's hourly rate
        updated_hourly_rate = 60.0
        update_result = update_teacher_in_mongo(self.collection_name, self.inserted_id, {"hourly_rate": updated_hourly_rate})
        self.assertTrue(update_result["acknowledged"], "Update was not acknowledged.")
        self.assertGreater(update_result["modified_count"], 0, "No documents were modified.")

        # Verify the update
        updated_teacher = get_teacher_from_mongo(self.collection_name, self.inserted_id)
        self.assertIsNotNone(updated_teacher, "Teacher not found after update.")
        self.assertEqual(updated_teacher.hourly_rate, updated_hourly_rate, "Updated hourly rate does not match.")

    def test_delete_teacher(self):
        # Delete the teacher
        delete_result = delete_teacher_from_mongo(self.collection_name, self.inserted_id)
        self.assertTrue(delete_result["acknowledged"], "Delete was not acknowledged.")
        self.assertEqual(delete_result["deleted_count"], 1, "No documents were deleted.")

        # Verify deletion
        deleted_teacher = get_teacher_from_mongo(self.collection_name, self.inserted_id)
        self.assertIsNone(deleted_teacher, "Teacher was not deleted.")


if __name__ == '__main__':
    unittest.main()
