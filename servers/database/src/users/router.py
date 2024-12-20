from fastapi import APIRouter, Body

from servers.database.src.users.service import usersDbRequests


users_router = APIRouter()


@users_router.post("/auth")
async def auth_user_endpoint(data=Body(...)):
    await usersDbRequests.SQL_insert_user(data)
    return None


@users_router.post("/get-user-details")
async def user_details_endpoint(data=Body(...)):
    SQL_response = await usersDbRequests.SQL_get_user_details(data)
    return SQL_response