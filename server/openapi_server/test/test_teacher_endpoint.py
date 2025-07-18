import unittest
from fastapi.testclient import TestClient
from server.openapi_server.__main__ import app
from datetime import datetime

class TestTeacherEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Assuming your FastAPI app is initialized in a variable 'app'
        cls.client = TestClient(app)

    def test_get_all_teachers(self):
        response = self.client.get("/teachers/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)  # Check that a list is returned

    def test_create_teacher(self):
        new_teacher = {
            "name": "John Doe",
            "subjects": ["Math", "Science"],
            "hire_date": datetime.now().isoformat(),
            "email": "johndoe@example.com"
        }
        response = self.client.post("/teachers/", json=new_teacher)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], new_teacher['name'])  # Validate returned data

    def test_update_teacher(self):
        # First create a teacher to update
        new_teacher = {
            "name": "Jane Doe",
            "subjects": ["English"],
            "hire_date": datetime.now().isoformat(),
            "email": "janedoe@example.com"
        }
        create_resp = self.client.post("/teachers/", json=new_teacher)
        teacher_id = create_resp.json()['id']

        # Now update the teacher
        updates = {"name": "Jane Smith"}
        update_resp = self.client.put(f"/teachers/{teacher_id}", json=updates)
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.json()['name'], updates['name'])

    def test_delete_teacher(self):
        # First create a teacher to delete
        new_teacher = {
            "name": "Mike Johnson",
            "subjects": ["History"],
            "hire_date": datetime.now().isoformat(),
            "email": "mikej@example.com"
        }
        create_resp = self.client.post("/teachers/", json=new_teacher)
        teacher_id = create_resp.json()['id']

        # Now delete the teacher
        delete_resp = self.client.delete(f"/teachers/{teacher_id}")
        self.assertEqual(delete_resp.status_code, 200)
        self.assertEqual(delete_resp.json()['message'], "Teacher deleted successfully")

    def test_get_teacher_by_id(self):
        """Test GET /teachers/{id} endpoint to retrieve a teacher by ID."""
        # First, create a teacher
        new_teacher = {
            "name": "Alice Smith",
            "subjects": ["Art", "Music"],
            "hire_date": datetime.now().isoformat(),
            "email": "alice.smith@example.com"
        }
        create_resp = self.client.post("/teachers/", json=new_teacher)
        teacher_id = create_resp.json()['id']

        # Retrieve the teacher by ID
        get_resp = self.client.get(f"/teachers/{teacher_id}")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json()['name'], new_teacher['name'])

        # Clean up by deleting the teacher
        self.client.delete(f"/teachers/{teacher_id}")


if __name__ == '__main__':
    unittest.main()
