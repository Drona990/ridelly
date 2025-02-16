from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.schemas.auth_schemas import Token
from app.services.auth_services import send_email
from app.services.otp_services import OTPService
from app.utils.security import create_access_token
from app.models.profile_model import Profile  # Import your Profile model


async def request_otp(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    
    if user and not OTPService.can_resend_otp(user.otp_sent_at):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="OTP already sent. Please wait 5 minutes."
        )
        
    otp = OTPService.generate_otp()
    
    await send_email(email, otp)
        
    if not user:
        user = User(email=email, otp=otp, otp_sent_at=datetime.utcnow())
        db.add(user)
    else:
        user.otp = otp
        user.otp_sent_at = datetime.utcnow()
        
    db.commit()
    db.refresh(user)
    return {"message": "OTP sent successfully."}

async def verify_otp1(email: str, otp: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.otp != otp or not OTPService.is_otp_valid(user.otp_sent_at):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP.")
        
    user.is_verified = True
    user.otp = None
    user.otp_sent_at = None
    db.commit()

    token = create_access_token({"user_id": str(user.user_id), "email": user.email})
    return {"access_token": token, "token_type": "Bearer"}


async def verify_otp(email: str, otp: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or user.otp != otp or not OTPService.is_otp_valid(user.otp_sent_at):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP.")
    
    # ✅ Mark user as verified
    user.is_verified = True
    user.otp = None
    user.otp_sent_at = None
    db.commit()

    # Check if profile exists
    profile = db.query(Profile).filter(Profile.user_id == user.user_id).first()
    if not profile:
        return {
            "message": "OTP verified successfully. Please create your profile.",
            "user_id": str(user.user_id),
            "email": user.email
        }

    # Generate access token if profile exists
    token = create_access_token({"user_id": str(user.user_id), "email": user.email})
    return {"access_token": token, "token_type": "Bearer"}
