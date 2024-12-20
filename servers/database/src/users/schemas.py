from pydantic import BaseModel


class AddUser(BaseModel):
    user_id: str


class GetApplications(BaseModel):
    user_id: str


class GetUser(BaseModel):
    user_id: str