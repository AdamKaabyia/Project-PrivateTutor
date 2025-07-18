# import unittest
#
# from flask import json
#
# from openapi_server.models.meeting import Meeting  # noqa: E501
# from openapi_server.models.person import Person  # noqa: E501
# from openapi_server.models.student import Student  # noqa: E501
# from openapi_server.models.teacher import Teacher  # noqa: E501
# from openapi_server.test import BaseTestCase
#
#
# class TestDefaultController(BaseTestCase):
#     """DefaultController integration test stubs"""
#
#     def test_auth_callback_google_get(self):
#         """Test case for auth_callback_google_get
#
#         Google OAuth2 Callback
#         """
#         query_string = [('code', 'code_example')]
#         headers = {
#         }
#         response = self.client.open(
#             '/auth/callback/google',
#             method='GET',
#             headers=headers,
#             query_string=query_string)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_auth_login_google_get(self):
#         """Test case for auth_login_google_get
#
#         Login via Google
#         """
#         headers = {
#         }
#         response = self.client.open(
#             '/auth/login/google',
#             method='GET',
#             headers=headers)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_meetings_get(self):
#         """Test case for meetings_get
#
#         Get a list of all meetings
#         """
#         headers = {
#             'Accept': 'application/json',
#         }
#         response = self.client.open(
#             '/meetings',
#             method='GET',
#             headers=headers)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_meetings_post(self):
#         """Test case for meetings_post
#
#         Create a new meeting
#         """
#         meeting = {"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]}
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         response = self.client.open(
#             '/meetings',
#             method='POST',
#             headers=headers,
#             data=json.dumps(meeting),
#             content_type='application/json')
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_meetings_schedule_google_calendar_post(self):
#         """Test case for meetings_schedule_google_calendar_post
#
#         Schedule a meeting in Google Calendar
#         """
#         meeting = {"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]}
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         response = self.client.open(
#             '/meetings/schedule-google-calendar',
#             method='POST',
#             headers=headers,
#             data=json.dumps(meeting),
#             content_type='application/json')
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_persons_get(self):
#         """Test case for persons_get
#
#         Get a list of all persons
#         """
#         headers = {
#             'Accept': 'application/json',
#         }
#         response = self.client.open(
#             '/persons',
#             method='GET',
#             headers=headers)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_students_delete(self):
#         """Test case for students_delete
#
#         Delete a student by ID
#         """
#         query_string = [('id', 56)]
#         headers = {
#         }
#         response = self.client.open(
#             '/students',
#             method='DELETE',
#             headers=headers,
#             query_string=query_string)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_students_get(self):
#         """Test case for students_get
#
#         Get a list of all students
#         """
#         headers = {
#             'Accept': 'application/json',
#         }
#         response = self.client.open(
#             '/students',
#             method='GET',
#             headers=headers)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_students_post(self):
#         """Test case for students_post
#
#         Create a new student
#         """
#         student = {"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"subjects_interested_in_learning":["subjects_interested_in_learning","subjects_interested_in_learning"],"meetings":[{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]},{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]}],"id":0,"email":"email"}
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         response = self.client.open(
#             '/students',
#             method='POST',
#             headers=headers,
#             data=json.dumps(student),
#             content_type='application/json')
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_students_put(self):
#         """Test case for students_put
#
#         Update student details
#         """
#         student = {"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"subjects_interested_in_learning":["subjects_interested_in_learning","subjects_interested_in_learning"],"meetings":[{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]},{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]}],"id":0,"email":"email"}
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         response = self.client.open(
#             '/students',
#             method='PUT',
#             headers=headers,
#             data=json.dumps(student),
#             content_type='application/json')
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_teachers_delete(self):
#         """Test case for teachers_delete
#
#         Delete a teacher by ID
#         """
#         query_string = [('id', 56)]
#         headers = {
#         }
#         response = self.client.open(
#             '/teachers',
#             method='DELETE',
#             headers=headers,
#             query_string=query_string)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_teachers_get(self):
#         """Test case for teachers_get
#
#         Get a list of all teachers
#         """
#         headers = {
#             'Accept': 'application/json',
#         }
#         response = self.client.open(
#             '/teachers',
#             method='GET',
#             headers=headers)
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_teachers_post(self):
#         """Test case for teachers_post
#
#         Create a new teacher
#         """
#         teacher = {"about_section":"about_section","phone":"phone","hourly_rate":6.0274563,"name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"subjects_to_teach":["subjects_to_teach","subjects_to_teach"],"meetings":[{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]},{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]}],"id":0,"email":"email"}
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         response = self.client.open(
#             '/teachers',
#             method='POST',
#             headers=headers,
#             data=json.dumps(teacher),
#             content_type='application/json')
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#     def test_teachers_put(self):
#         """Test case for teachers_put
#
#         Update teacher details
#         """
#         teacher = {"about_section":"about_section","phone":"phone","hourly_rate":6.0274563,"name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"subjects_to_teach":["subjects_to_teach","subjects_to_teach"],"meetings":[{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]},{"start_time":"2000-01-23T04:56:07.000+00:00","subject":"subject","location":"location","people":[{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"},{"about_section":"about_section","phone":"phone","name":"name","available":["2000-01-23T04:56:07.000+00:00","2000-01-23T04:56:07.000+00:00"],"rating":4.5,"id":0,"email":"email"}],"finish_time":"2000-01-23T04:56:07.000+00:00","attached_files":["",""]}],"id":0,"email":"email"}
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         response = self.client.open(
#             '/teachers',
#             method='PUT',
#             headers=headers,
#             data=json.dumps(teacher),
#             content_type='application/json')
#         self.assert200(response,
#                        'Response body is : ' + response.data.decode('utf-8'))
#
#
# if __name__ == '__main__':
#     unittest.main()
