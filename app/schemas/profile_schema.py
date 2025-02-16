from pydantic import BaseModel
from uuid import UUID

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class ProfileResponse(ProfileCreate):
    user_id: UUID
    email: str

class ProfileCreateRequest(ProfileCreate):
    user_id: str
    email: str

class ProfileWithTokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    profile: ProfileResponse
