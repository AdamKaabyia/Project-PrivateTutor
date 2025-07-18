import unittest
from datetime import datetime

from bson import ObjectId
from server.openapi_server.models.DB_utils import (
    create_user,
    get_users_by_username,
    authenticate_user,
    update_user,
    delete_user,
    hash_password,
    mongo_db,
    get_user_by_id,
)
from server.openapi_server.models.user import User


class TestUserMongoOperations(unittest.TestCase):
    """Integration tests for User MongoDB operations."""

    @classmethod
    def setUpClass(cls):
        """Set up MongoDB connection."""
        cls.db = mongo_db.get_collection("users")

    def setUp(self):
        """Clean up before each test."""
        self.db.delete_many({})

    def tearDown(self):
        """Clean up after each test."""
        self.db.delete_many({})

    def seed_user(self, username, password="defaultpassword", **kwargs):
        """Insert a user into the database."""
        user = User(
            username=username,
            password=hash_password(password),
            roles=kwargs.get("roles", ["student"]),
            name=kwargs.get("name", "Default Name"),
            email=kwargs.get("email", f"{username}@example.com"),
            created_at=kwargs.get("created_at", datetime.utcnow()),  # Set current timestamp
        )
        user_data = user.model_dump(by_alias=True, exclude_none=True)
        return str(self.db.insert_one(user_data).inserted_id)

    def test_create_user(self):
        """Test user creation."""
        user = User(
            username="john_doe",
            email="john.doe@example.com",
            password="securepassword123",
            roles=["student", "teacher"],
            name="John Doe",
        )
        user_id = create_user("users", user)
        self.assertIsNotNone(user_id)

        user_in_db = self.db.find_one({"_id": ObjectId(user_id)})
        self.assertIsNotNone(user_in_db)
        self.assertEqual(user_in_db["username"], "john_doe")

    def test_get_users_by_username(self):
        """Test retrieving multiple users by the same username."""
        # Seed multiple users with the same username
        user1_id = self.seed_user("jane_doe", "password1", email="jane1@example.com")
        user2_id = self.seed_user("jane_doe", "password2", email="jane2@example.com")

        # Call the function
        retrieved_users = get_users_by_username("users", "jane_doe")

        # Validate the results
        self.assertIsInstance(retrieved_users, list)
        self.assertEqual(len(retrieved_users), 2)  # Should return both users

        # Check the data of the retrieved users
        user_ids = {str(user.id) for user in retrieved_users}  # Access `user.id`
        self.assertIn(user1_id, user_ids)
        self.assertIn(user2_id, user_ids)

        emails = {user.email for user in retrieved_users}
        self.assertIn("jane1@example.com", emails)
        self.assertIn("jane2@example.com", emails)

    def test_authenticate_user(self):
        """Test authenticating a user."""
        # Seed two users with different emails
        self.seed_user("john_doe", "password1", email="john1@example.com", created_at=datetime.utcnow())
        self.seed_user("john_doe", "password2", email="john2@example.com", created_at=datetime.utcnow())

        # Authenticate the first user by email
        authenticated_user = authenticate_user("users", "john1@example.com", "password1")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.email, "john1@example.com")

        # Authenticate the second user by email
        authenticated_user = authenticate_user("users", "john2@example.com", "password2")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.email, "john2@example.com")

    def test_update_user(self):
        """Test updating a user."""
        # Seed a user
        user_id = self.seed_user("john_doe", "securepassword123")
        updates = {"about_section": "Updated profile"}

        # Update the user
        result = update_user("users", user_id, updates)
        self.assertTrue(result)

        updated_user = self.db.find_one({"_id": ObjectId(user_id)})
        self.assertEqual(updated_user["about_section"], "Updated profile")

    def test_delete_user(self):
        """Test deleting a user."""
        # Seed a user
        user_id = self.seed_user("john_doe", "securepassword123")

        # Delete the user
        result = delete_user("users", user_id)
        self.assertTrue(result)

        deleted_user = self.db.find_one({"_id": ObjectId(user_id)})
        self.assertIsNone(deleted_user)

    def test_get_nonexistent_user(self):
        """Test fetching a user that does not exist."""
        nonexistent_id = str(ObjectId())
        retrieved_user = get_user_by_id("users", nonexistent_id)
        self.assertIsNone(retrieved_user)

    def test_get_user_by_id(self):
        """Test fetching a user by MongoDB's ObjectId."""
        # Seed a user
        user_id = self.seed_user("john_doe", "password123")

        # Fetch the user by the MongoDB ObjectId
        retrieved_user = get_user_by_id("users", user_id)

        # Validate the retrieved user
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(str(retrieved_user.id), user_id)  # Access `user.id`
        self.assertEqual(retrieved_user.username, "john_doe")


if __name__ == "__main__":
    unittest.main()
