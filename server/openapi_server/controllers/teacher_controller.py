from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException
from pymongo.errors import OperationFailure
from bson import ObjectId

from server.openapi_server.models.DB_utils import (
    save_teacher_to_mongo,
    get_teacher_from_mongo,
    update_teacher_in_mongo,
    delete_teacher_from_mongo,
    mongo_db
)
from server.openapi_server.models.teacher import Teacher

teachers_router = APIRouter()

@teachers_router.get("/", response_model=list[Teacher])
def get_all_teachers():
    """Retrieve all teachers."""
    try:
        collection = mongo_db.get_collection("teachers")
        teachers = list(collection.find({}, {'_id': 0}))  # Exclude `_id` field from the results
        return [Teacher(**teacher) for teacher in teachers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@teachers_router.post("/", response_model=Teacher)
def create_teacher(teacher: Teacher):
    """Create a new teacher and return the full teacher object."""
    try:
        result = save_teacher_to_mongo('teachers', teacher)
        if result.get("acknowledged"):
            teacher.id = str(result.get("inserted_id"))  # Set the Mongo-generated ID into the returned model
            return teacher  # ✅ Return the validated Teacher object
        raise HTTPException(status_code=500, detail="Failed to create teacher.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating teacher: {str(e)}")



@teachers_router.put("/{id}", response_model=Teacher)
def update_teacher(id: str, teacher: Teacher):
    """Update a teacher's details."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    try:
        result = update_teacher_in_mongo('teachers', id, teacher.model_dump(exclude_unset=True))
        if result.get("acknowledged") and result.get("modified_count"):
            # ✅ Fetch updated document from Mongo
            updated_doc = mongo_db.get_collection("teachers").find_one({"_id": ObjectId(id)})
            if updated_doc:
                updated_doc["id"] = str(updated_doc["_id"])  # Convert for Pydantic model
                return Teacher(**updated_doc)

        raise HTTPException(status_code=404, detail="Teacher not found or no changes made")

    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    except OperationFailure as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Operation Failure: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teachers_router.delete("/{id}")
def delete_teacher(id: str):
    """Delete a teacher by ID."""
    try:
        result = delete_teacher_from_mongo('teachers', id)
        if result.get("deleted_count"):
            return {"message": "Teacher deleted successfully"}
        raise HTTPException(status_code=404, detail="Teacher not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@teachers_router.get("/{id}", response_model=Teacher)
def get_teacher_by_id(id: str):
    """Retrieve a single teacher by ID."""
    try:
        teacher_doc = get_teacher_from_mongo('teachers', id)
        if not teacher_doc:
            raise HTTPException(status_code=404, detail="Teacher not found")

        teacher = Teacher(**teacher_doc)  # Create Pydantic model
        return teacher.model_dump()       # ✅ Return dict, not model!
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

