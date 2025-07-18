from fastapi import FastAPI
import uvicorn

from server.openapi_server.controllers.meeting_controller import meetings_router
from server.openapi_server.controllers.student_controller import students_router
from server.openapi_server.controllers.teacher_controller import teachers_router
from server.openapi_server.controllers.user_controller import user_router

app = FastAPI(title="Student-Teacher Meeting Scheduler API")

# Include Routers
app.include_router(meetings_router, prefix="/meetings", tags=["Meetings"])
app.include_router(students_router, prefix="/students", tags=["Students"])
app.include_router(teachers_router, prefix="/teachers", tags=["Teachers"])
app.include_router(user_router, prefix="/users")  # <<<< this line is crucial

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
