from fastapi import APIRouter, Body

from servers.database.src.applications.service import applicationsDbRequests

applications_router = APIRouter()


@applications_router.post("/get-applications")
async def auth_endpoint(data=Body(...)):
    SQL_response = await applicationsDbRequests.SQL_get_applications(data)
    return SQL_response


@applications_router.post("/get-application-details")
async def auth_endpoint(data=Body(...)):
    SQL_response = await applicationsDbRequests.SQL_get_application_details(data)
    return SQL_response