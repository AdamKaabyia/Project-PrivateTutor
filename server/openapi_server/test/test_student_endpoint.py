import unittest
from fastapi.testclient import TestClient
from server.openapi_server.__main__ import app

client = TestClient(app)


class TestStudentsEndpoints(unittest.TestCase):
    def setUp(self):
        """Create a test student before each test."""
        self.student_payload = {
            "name": "John Doe",
            "phone": "1234567890",
            "email": "johndoe@example.com",
            "about_section": "A curious learner passionate about technology.",
            "available": ["2024-12-13T10:00:00Z", "2024-12-14T15:00:00Z"],
            "rating": 4.5,
            "subjects_interested_in_learning": ["Math", "Physics", "Programming"],
            "meetings": [
                {"meeting_id": "1234", "date": "2024-12-15T10:00:00Z"}
            ],
        }
        response = client.post("/students/", json=self.student_payload)
        self.assertEqual(response.status_code, 200)
        self.student_id = response.json()["id"]

    def tearDown(self):
        """Delete the test student after each test."""
        response = client.delete(f"/students/{self.student_id}")
        self.assertIn(response.status_code, [200, 404])  # Allow if already deleted.

    def test_create_student(self):
        """Test POST /students/ to create a new student."""
        response = client.post("/students/", json=self.student_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertIn("id", response.json())

    def test_get_students(self):
        """Test GET /students/ to retrieve all students."""
        response = client.get("/students/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_student_by_id(self):
        """Test GET /students/{id} to retrieve a specific student by ID."""
        response = client.get(f"/students/{self.student_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json().get("id"), self.student_id)

    def test_update_student(self):
        """Test PUT /students/{id} to update a student's details."""
        update_payload = {
            "name": "Jane Doe",
            "rating": 4.8,
        }
        response = client.put(f"/students/{self.student_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

        # Verify the update
        response = client.get(f"/students/{self.student_id}")
        self.assertEqual(response.json()["name"], "Jane Doe")
        self.assertEqual(response.json()["rating"], 4.8)

    def test_delete_student(self):
        """Test DELETE /students/{id} to delete a student."""
        response = client.delete(f"/students/{self.student_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

        # Verify deletion
        response = client.get(f"/students/{self.student_id}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
