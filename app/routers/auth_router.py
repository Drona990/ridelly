from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth_controller import request_otp,verify_otp
from app.schemas.auth_schemas import UserCreate , OTPRequest

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/request-otp")
async def request_otp_handler(user:UserCreate, db: Session = Depends(get_db)):
    return await request_otp(db,user.email)


@router.post("/verify-otp")
async def verify_otp_handler(user:OTPRequest, db: Session = Depends(get_db)):
    return await verify_otp(user.email, user.otp, db)
    