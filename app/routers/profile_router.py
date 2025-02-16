from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.profile_controller import create_or_update_profile, get_profile
from app.schemas.profile_schema import ProfileCreate, ProfileCreateRequest, ProfileResponse, ProfileWithTokenResponse
from app.utils.security import create_access_token, get_current_user
from app.models.user_model import User 
import uuid


router = APIRouter(prefix="/api/v1/profiles", tags=["Profiles"])

@router.post("/createProfile", response_model=ProfileResponse)
def create_user_profile(
    profile: ProfileCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return create_or_update_profile(db, current_user["user_id"], current_user["email"],profile)

@router.get("/getProfile", response_model=ProfileResponse)
def get_user_profile(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return get_profile(db, current_user["user_id"])

@router.post("/public/createProfile", response_model=ProfileWithTokenResponse)
def create_user_profile_public(
    profile_data: ProfileCreateRequest,  
    db: Session = Depends(get_db)
):
    try:
        user_uuid = uuid.UUID(profile_data.user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for user_id")

    user = db.query(User).filter(User.user_id == user_uuid, User.email == profile_data.email).first()
    
    if not user or not user.is_verified:
        raise HTTPException(status_code=403, detail="User has not verified OTP. Profile creation denied.")

    profile = create_or_update_profile(db, user_uuid, profile_data.email, profile_data)
    
    token = create_access_token({"user_id": str(profile.user_id), "email": profile.email})

    return ProfileWithTokenResponse(
        message="Profile created successfully",
        access_token=token,
        token_type="Bearer",
        profile=ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            email=profile.email,
            first_name=profile.first_name,
            last_name=profile.last_name
        )
    )