# Insert data into the 'users' collection
from server.openapi_server.models.DB_utils import insert_data, find_one_data, find_data


user_data = {"name": "John Doe", "email": "john@example.com"}
insert_data("users", user_data)

# Insert multiple documents
users_data = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]
insert_data("users", users_data)

# Query for a single user
query = {"name": "Alice"}
user = find_one_data("users", query)
print("Found user:", user)

# Query for all users
all_users = find_data("users", {})
print("All users:", all_users)
