# coding: utf-8

"""
    Private Tutor Scheduling API

    API for private tutors to manage their schedules and for students to book tutoring sessions.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from apis.default_api import router as DefaultApiRouter

app = FastAPI(
    title="Private Tutor Scheduling API",
    description="API for private tutors to manage their schedules and for students to book tutoring sessions.",
    version="1.0.0",
)

app.include_router(DefaultApiRouter)
