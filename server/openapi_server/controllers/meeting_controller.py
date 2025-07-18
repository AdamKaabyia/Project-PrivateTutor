from fastapi import APIRouter, HTTPException, status
from server.openapi_server.models.DB_utils import (
    save_meeting_to_mongo,
    get_meeting_from_mongo,
    update_meeting_in_mongo,
    delete_meeting_from_mongo,
    mongo_db
)
from server.openapi_server.models.meeting import Meeting

meetings_router = APIRouter()

@meetings_router.get("/", response_model=list[Meeting])
def get_all_meetings():
    """Retrieve all meetings."""
    try:
        collection = mongo_db.get_collection("meetings")
        meetings = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB's `_id` field
        return [Meeting.model_validate(meeting) for meeting in meetings]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@meetings_router.post("/", response_model=dict)
def create_meeting(meeting: Meeting):
    """Create a new meeting."""
    try:
        result = save_meeting_to_mongo('meetings', meeting)
        if result.get("acknowledged"):
            return {"message": "Meeting created successfully", "id": str(result.get("inserted_id"))}
        raise HTTPException(status_code=500, detail="Failed to create meeting")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@meetings_router.put("/{id}", response_model=dict)
def update_meeting(id: str, meeting: Meeting):
    """Update an existing meeting."""
    try:
        update_data = meeting.model_dump()
        result = update_meeting_in_mongo('meetings', id, update_data)

        if not result.get("acknowledged"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

        if result.get("modified_count") == 0:
            # Even if the operation is acknowledged but no document is modified,
            # it can be due to sending an update that matches the existing data.
            # This might not necessarily be an error depending on your application's requirements.
            return {"message": "No changes were made", "status": "warning"}

        return {"message": "Meeting updated successfully", "status": "success"}

    except Exception as e:
        # Log the exception details here to help with debugging
        print(f"Error updating meeting: {e}")  # Consider using a proper logging framework
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")


@meetings_router.delete("/{id}", response_model=dict)
def delete_meeting(id: str):
    """Delete a meeting by ID."""
    try:
        result = delete_meeting_from_mongo('meetings', id)
        if result.get("deleted_count"):
            return {"message": "Meeting deleted successfully"}
        raise HTTPException(status_code=404, detail="Meeting not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@meetings_router.get("/{id}", response_model=Meeting)
def get_meeting_by_id(id: str):
    """Retrieve a specific meeting by ID."""
    try:
        meeting = get_meeting_from_mongo('meetings', id)
        if meeting:
            return Meeting.model_validate(meeting)
        else:
            raise HTTPException(status_code=404, detail="Meeting not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
