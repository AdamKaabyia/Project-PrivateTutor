import unittest
from fastapi.testclient import TestClient
from bson import ObjectId
from server.openapi_server.controllers.user_controller import user_router
from server.openapi_server.models.DB_utils import create_user, delete_user
from server.openapi_server.models.user import User
from fastapi import FastAPI
import uuid

app = FastAPI()
app.include_router(user_router, prefix="/users")
client = TestClient(app)

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.test_username = f"user_{uuid.uuid4().hex[:8]}"
        self.test_email = f"{self.test_username}@example.com"
        self.test_password = "password123"
        self.test_user = User(
            username=self.test_username,
            email=self.test_email,
            password=self.test_password,
            roles=["student"],
            name="Test User"
        )
        self.test_user_id = str(create_user("users", self.test_user))

    def tearDown(self):
        delete_user("users", self.test_user_id)

    def test_create_user(self):
        payload = {
            "username": f"user_{uuid.uuid4().hex[:8]}",
            "email": f"user_{uuid.uuid4().hex[:8]}@example.com",
            "password": "securepassword123",
            "roles": ["student"],
            "name": "New User"
        }
        response = client.post("/users", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("user_id", response.json())
        self.assertTrue(ObjectId.is_valid(response.json()["user_id"]))

    def test_delete_user(self):
        response = client.delete(f"/users/{self.test_user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User deleted successfully")

    def test_get_user_by_id(self):
        response = client.get(f"/users/id/{self.test_user_id}")
        self.assertEqual(response.status_code, 200)  # Expecting 200
        self.assertEqual(response.json()["username"], self.test_username)

    def test_get_users_by_username(self):
        response = client.get(f"/users/{self.test_username}")
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertGreaterEqual(len(users), 1)
        self.assertTrue(any(user["_id"] == self.test_user_id for user in users))

    def test_authenticate_user(self):
        payload = {"email": self.test_email, "password": self.test_password}
        response = client.post("/users/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], self.test_email)

    def test_update_user(self):
        payload = {"about_section": "Updated profile"}
        response = client.put(f"/users/{self.test_user_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User updated successfully")
