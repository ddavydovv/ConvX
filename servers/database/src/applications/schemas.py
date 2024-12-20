from pydantic import BaseModel


class AddApplication(BaseModel):
    user_id: str
    message_id: str
    category: str
    mode: str
    filename: str
    new_filename: str
    file_path: str
    create_at: str
    processed_at: str


class GetApplications(BaseModel):
    user_id: str