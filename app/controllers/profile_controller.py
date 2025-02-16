from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.profile_model import Profile
from app.schemas.profile_schema import ProfileCreate
import uuid

def create_or_update_profile(db: Session, user_id: uuid.UUID, email:str, profile_data: ProfileCreate):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    
    if profile:
        profile.first_name = profile_data.first_name
        profile.last_name = profile_data.last_name
    else:
        profile = Profile(
            user_id = user_id,
            email = email,
            first_name = profile_data.first_name,
            last_name = profile_data.last_name
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return profile

def get_profile(db: Session, user_id: uuid.UUID):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    print(profile)
    if not profile:
        return JSONResponse(status_code=404, content={"success":False, "message": "Profile not found."})
    return profile
