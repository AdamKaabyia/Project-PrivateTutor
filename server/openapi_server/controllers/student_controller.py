from fastapi import APIRouter, HTTPException
from typing import List
from server.openapi_server.models.DB_utils import (
    save_student_to_mongo,
    get_student_from_mongo,
    update_student_in_mongo,
    delete_student_from_mongo,
    mongo_db
)
from server.openapi_server.models.student import Student
from bson.errors import InvalidId
from bson import ObjectId

students_router = APIRouter()


# Works
@students_router.get("/", response_model=List[Student])
def get_all_students():
    """Retrieve all students."""
    try:
        collection = mongo_db.get_collection("students")
        students = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's `_id` field
        return [Student(**student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving students: {str(e)}")


# Works
@students_router.post("/", response_model=Student)
def create_student(student: Student):
    """Create a new student."""
    try:
        result = save_student_to_mongo('students', student)
        if result.get("acknowledged"):
            student.id = str(result.get("inserted_id"))  # update with ID from Mongo
            return student  # return full Student object
        raise HTTPException(status_code=500, detail="Failed to create student.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {str(e)}")


# Works
@students_router.put("/{id}", response_model=Student)
def update_student(id: str, student: Student):
    """Update an existing student."""
    try:
        try:
            object_id = ObjectId(id)  # Validate and convert the ID
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid student ID format.")

        # Update the student in MongoDB
        result = update_student_in_mongo('students', str(object_id), student.model_dump(exclude_unset=True))

        if result.get("acknowledged") and result.get("modified_count"):
            # ✅ Fetch and return the updated Student object
            updated_doc = mongo_db.get_collection("students").find_one({"_id": object_id})
            if updated_doc:
                updated_doc["id"] = str(updated_doc["_id"])  # Convert ObjectId to string for response
                return Student(**updated_doc)

        raise HTTPException(status_code=404, detail="Student not found or no changes detected.")

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")


# Works
@students_router.delete("/{student_id}", response_model=dict)
def delete_student(student_id: str):
    """Delete a student by ID."""
    try:
        try:
            object_id = ObjectId(student_id)  # Validate and convert the ID
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid student ID format.")
        result = delete_student_from_mongo("students", str(object_id))
        if result["deleted_count"] == 0:
            raise HTTPException(status_code=404, detail="Student not found.")
        return {"message": "Student deleted successfully."}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")


# Works
@students_router.get("/{id}", response_model=Student)
def get_student_by_id(id: str):
    """Retrieve a single student by ID."""
    try:
        student_doc = get_student_from_mongo('students', id)

        if not student_doc:
            raise HTTPException(status_code=404, detail="Student not found")

        # Ensure it's a dict before unpacking
        if isinstance(student_doc, Student):
            student_doc = student_doc.model_dump()

        return Student(**student_doc).model_dump()  # ✅ Pydantic-safe dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving student: {e}")

