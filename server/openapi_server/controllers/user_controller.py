from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

from server.openapi_server.models.user import User
from server.openapi_server.models.update_user_request import UpdateUserRequest
from server.openapi_server.models.DB_utils import (
    create_user,
    get_users_by_username,
    authenticate_user,
    delete_user,
    get_user_by_id,
    update_user,
    validate_object_id,
)

user_router = APIRouter()   # no prefix here


class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    roles: List[str] = Field(default_factory=list)
    name: str = Field(..., max_length=100)


class AuthenticateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


@user_router.post("/", status_code=201)
async def create_user_endpoint(request: CreateUserRequest):
    """Create a new user."""
    try:
        user = User(**request.dict())
        user_id = create_user("users", user)
        return {"message": "User created successfully", "user_id": str(user_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")


@user_router.post("/login")
async def authenticate_user_endpoint(request: AuthenticateUserRequest):
    """Authenticate a user by email and password."""
    try:
        user = authenticate_user("users", request.email, request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "message": "Authentication successful",
            "user_id": str(user.id),
            "email": user.email,
            "roles": user.roles,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during authentication: {e}")


@user_router.get("/id/{user_id}", response_model=User)
async def get_user_by_id_endpoint(user_id: str):
    """Retrieve a single user by ID."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format.")
    try:
        user = get_user_by_id("users", user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {e}")


@user_router.get("/{username}")
async def get_users_by_username_endpoint(username: str):
    """Retrieve all users by their username."""
    try:
        users = get_users_by_username("users", username)
        if not users:
            raise HTTPException(status_code=404, detail="No users found with this username")
        # Return a list of dicts; FastAPI will auto-encode
        return [u.dict(by_alias=True) for u in users]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")


@user_router.delete("/{user_id}")
async def delete_user_endpoint(user_id: str):
    """Delete a user."""
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format.")
    try:
        success = delete_user("users", user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")


@user_router.put(
    "/{user_id}",
    response_model=User,
    responses={
        400: {"description": "Invalid ID or no fields provided"},
        404: {"description": "User not found"},
        500: {"description": "Server error"},
    },
)
async def update_user_endpoint(user_id: str, request: UpdateUserRequest):
    """
    Update a user's details (partial update).
    Only fields provided in the body will be set.
    Returns the updated User.
    """
    # 1) Validate & coerce the ID
    try:
        validate_object_id(user_id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    # 2) Extract only the provided fields
    updates = request.dict(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    # 3) Apply the update
    try:
        success = update_user("users", user_id, updates)
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    # 4) Fetch & return the new record
    user = get_user_by_id("users", user_id)
    if not user:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated user")
    return user
