# import connexion
# from typing import Dict, Tuple, Union, List
# from flask import request
#
# from server.openapi_server.models.DB_utils import (
#     save_meeting_to_mongo,
#     get_meeting_from_mongo,
#     delete_meeting_from_mongo,
#     update_meeting_in_mongo,
#     save_student_to_mongo,
#     get_student_from_mongo,
#     delete_student_from_mongo,
#     update_student_in_mongo,
#     save_teacher_to_mongo,
#     get_teacher_from_mongo,
#     delete_teacher_from_mongo,
#     update_teacher_in_mongo,
#     mongo_db
# )
# from server.openapi_server.models.meeting import Meeting
# from server.openapi_server.models.student import Student
# from server.openapi_server.models.teacher import Teacher
#
#
# def auth_callback_google_get(code):
#     return 'Not implemented yet', 501
#
# def auth_login_google_get():
#     return 'Not implemented yet', 501
#
# def meetings_schedule_google_calendar_post(meeting):
#     return 'Not implemented yet', 501
#
# def meetings_get():
#     try:
#         meetings_collection = mongo_db.get_collection('meetings')
#         meetings = list(meetings_collection.find({}, {'_id': 0}))
#         return meetings, 200
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def meetings_post():
#     try:
#         if request.is_json:
#             meeting_data = request.get_json()
#             result = save_meeting_to_mongo('meetings', Meeting.from_dict(meeting_data))
#             if result.get("acknowledged"):
#                 return {'message': 'Meeting created successfully'}, 201
#         return {'error': 'Request must be JSON'}, 400
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def persons_get():
#     return 'Not implemented yet', 501
#
# def students_delete(id):
#     try:
#         result = delete_student_from_mongo('students', id)
#         if result.get("deleted_count"):
#             return {'message': 'Student deleted successfully'}, 200
#         return {'error': 'Student not found'}, 404
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def students_get():
#     try:
#         students_collection = mongo_db.get_collection('students')
#         students = list(students_collection.find({}, {'_id': 0}))
#         return students, 200
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def students_post():
#     try:
#         if request.is_json:
#             student_data = request.get_json()
#             result = save_student_to_mongo('students', Student.from_dict(student_data))
#             if result.get("acknowledged"):
#                 return {'message': 'Student created successfully'}, 201
#         return {'error': 'Request must be JSON'}, 400
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def students_put():
#     try:
#         if request.is_json:
#             student_data = request.get_json()
#             result = update_student_in_mongo('students', student_data.get('id'), student_data)
#             if result.get("acknowledged") and result.get("modified_count"):
#                 return {'message': 'Student updated successfully'}, 200
#         return {'error': 'Request must be JSON or Student not found'}, 400
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def teachers_delete(id):
#     try:
#         result = delete_teacher_from_mongo('teachers', id)
#         if result.get("deleted_count"):
#             return {'message': 'Teacher deleted successfully'}, 200
#         return {'error': 'Teacher not found'}, 404
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def teachers_get():
#     try:
#         teachers_collection = mongo_db.get_collection('teachers')
#         teachers = list(teachers_collection.find({}, {'_id': 0}))
#         return teachers, 200
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def teachers_post():
#     try:
#         if request.is_json:
#             teacher_data = request.get_json()
#             result = save_teacher_to_mongo('teachers', Teacher.from_dict(teacher_data))
#             if result.get("acknowledged"):
#                 return {'message': 'Teacher created successfully'}, 201
#         return {'error': 'Request must be JSON'}, 400
#     except Exception as e:
#         return {'error': str(e)}, 500
#
# def teachers_put():
#     try:
#         if request.is_json:
#             teacher_data = request.get_json()
#             result = update_teacher_in_mongo('teachers', teacher_data.get('id'), teacher_data)
#             if result.get("acknowledged") and result.get("modified_count"):
#                 return {'message': 'Teacher updated successfully'}, 200
#         return {'error': 'Request must be JSON or Teacher not found'}, 400
#     except Exception as e:
#         return {'error': str(e)}, 500
