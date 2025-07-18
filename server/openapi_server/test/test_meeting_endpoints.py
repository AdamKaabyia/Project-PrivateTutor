import unittest
from fastapi.testclient import TestClient
from server.openapi_server.__main__ import app

client = TestClient(app)

class TestMeetingsEndpoints(unittest.TestCase):
    def create_meeting(self):
        """Utility method to create a meeting and return the ID."""
        meeting_payload = {
            "location": "Conference Room 1",
            "start_time": "2024-12-15T10:00:00Z",
            "finish_time": "2024-12-15T11:00:00Z",
            "subject": "Project Discussion",
            "people": [
                {"name": "Person A", "role": "Attendee"},
                {"name": "Person B", "role": "Attendee"}
            ],
            "attached_files": [
                {"file_name": "file1.pdf", "file_type": "PDF"},
                {"file_name": "file2.doc", "file_type": "Document"}
            ]
        }
        response = client.post("/meetings/", json=meeting_payload)
        if response.status_code == 200:
            return response.json()['id']
        else:
            self.fail("Failed to create meeting for testing: {}".format(response.json()))

    def delete_meeting(self, meeting_id):
        """Utility method to delete a meeting."""
        client.delete(f"/meetings/{meeting_id}")

    def test_get_all_meetings(self):
        """Test GET /meetings/ endpoint to retrieve all meetings."""
        response = client.get("/meetings/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_meeting(self):
        """Test POST /meetings/ endpoint to create a new meeting."""
        meeting_id = self.create_meeting()
        self.delete_meeting(meeting_id)  # Clean up immediately after creation

    def test_update_meeting(self):
        """Test PUT /meetings/{id} endpoint to update a meeting."""
        meeting_id = self.create_meeting()
        update_payload = {
            "location": "Updated Location",
            "start_time": "2024-12-15T12:00:00Z",
            "finish_time": "2024-12-15T13:00:00Z",
            "subject": "Updated Discussion",
            "people": [
                {"name": "Person E", "role": "Attendee"},
                {"name": "Person F", "role": "Attendee"}
            ],
            "attached_files": [
                {"file_name": "updated_file.pdf", "file_type": "PDF"}
            ]
        }
        response = client.put(f"/meetings/{meeting_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)  # Expecting successful update

    def test_delete_meeting(self):
        """Test DELETE /meetings/{id} endpoint to delete a meeting."""
        meeting_id = self.create_meeting()
        response = client.delete(f"/meetings/{meeting_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_meeting_by_id(self):
        """Test GET /meetings/{id} endpoint to retrieve a specific meeting by ID."""
        meeting_id = self.create_meeting()
        response = client.get(f"/meetings/{meeting_id}")
        self.assertEqual(response.status_code, 200)
        self.delete_meeting(meeting_id)  # Clean up immediately after retrieval

if __name__ == '__main__':
    unittest.main()
