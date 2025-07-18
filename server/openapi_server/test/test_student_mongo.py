import unittest
from datetime import datetime
from bson import ObjectId

from server.openapi_server.models.DB_utils import (
    save_student_to_mongo,
    get_student_from_mongo,
    update_student_in_mongo,
    delete_student_from_mongo,
    mongo_db
)
from server.openapi_server.models.student import Student


class TestStudentDbFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection_name = "test_students"
        cls.collection = mongo_db.get_collection(cls.collection_name)

    def setUp(self):
        self.collection.delete_many({})  # Clear the collection before each test

    def test_save_student(self):
        test_student = Student(
            id=str(ObjectId()),
            name="Jane Doe",
            phone="9876543210",
            email="janedoe@example.com",
            about_section="Test student",
            available=[datetime.now()],
            rating=4.8,
            subjects_interested_in_learning=["Math", "Science"],
            meetings=[]
        )

        # Save the test student to MongoDB
        result = save_student_to_mongo(self.collection_name, test_student)
        self.assertTrue(result["acknowledged"], "Save operation not acknowledged.")
        if result.get("inserted_id"):
            self.assertIn("inserted_id", result, "Student ID was not returned.")

            # Verify student saved in DB
            inserted_id = result["inserted_id"]
            student_in_db = self.collection.find_one({"_id": ObjectId(inserted_id)})
            self.assertIsNotNone(student_in_db, "Student was not saved to MongoDB.")
            self.assertEqual(student_in_db["name"], test_student.name, "Saved name does not match.")
        else:
            self.fail("Insert operation did not return an inserted ID.")

    def test_get_student(self):
        test_student = Student(
            id=str(ObjectId()),
            name="Jane Doe",
            phone="9876543210",
            email="janedoe@example.com",
            about_section="Test student",
            available=[datetime.now()],
            rating=4.8,
            subjects_interested_in_learning=["Math", "Science"],
            meetings=[]
        )

        # Save the test student to MongoDB
        save_result = save_student_to_mongo(self.collection_name, test_student)
        inserted_id = save_result["inserted_id"]

        # Retrieve the student using its ID
        retrieved_student = get_student_from_mongo(self.collection_name, inserted_id)
        self.assertIsNotNone(retrieved_student, "Student not found.")
        self.assertEqual(retrieved_student.name, test_student.name, "Name does not match.")
        self.assertEqual(retrieved_student.email, test_student.email, "Email does not match.")

    def test_update_student(self):
        test_student = Student(
            id=str(ObjectId()),
            name="Jane Doe",
            phone="9876543210",
            email="janedoe@example.com",
            about_section="Test student",
            available=[datetime.now()],
            rating=4.8,
            subjects_interested_in_learning=["Math", "Science"],
            meetings=[]
        )

        # Save the test student to MongoDB
        save_result = save_student_to_mongo(self.collection_name, test_student)
        inserted_id = save_result["inserted_id"]

        # Update the student's phone number
        updated_phone = "1231231234"
        update_result = update_student_in_mongo(self.collection_name, inserted_id, {"phone": updated_phone})
        self.assertTrue(update_result["acknowledged"], "Update operation not acknowledged.")
        self.assertGreater(update_result["modified_count"], 0, "No documents were modified.")

        # Verify the update
        updated_student = get_student_from_mongo(self.collection_name, inserted_id)
        self.assertIsNotNone(updated_student, "Student not found after update.")
        self.assertEqual(updated_student.phone, updated_phone, "Updated phone does not match.")

    def test_delete_student(self):
        test_student = Student(
            id=str(ObjectId()),
            name="Jane Doe",
            phone="9876543210",
            email="janedoe@example.com",
            about_section="Test student",
            available=[datetime.now()],
            rating=4.8,
            subjects_interested_in_learning=["Math", "Science"],
            meetings=[]
        )

        # Save the test student to MongoDB
        save_result = save_student_to_mongo(self.collection_name, test_student)
        inserted_id = save_result["inserted_id"]

        # Delete the student
        delete_result = delete_student_from_mongo(self.collection_name, inserted_id)
        self.assertTrue(delete_result["acknowledged"], "Delete operation not acknowledged.")
        self.assertEqual(delete_result["deleted_count"], 1, "No documents were deleted.")

        # Verify deletion
        deleted_student = get_student_from_mongo(self.collection_name, inserted_id)
        self.assertIsNone(deleted_student, "Student was not deleted.")

    def tearDown(self):
        self.collection.delete_many({})  # Clean up after each test


if __name__ == '__main__':
    unittest.main()
