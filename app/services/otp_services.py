import random
from datetime import datetime, timedelta

class OTPService:
    OTP_VALIDITY_MINUTES = 5

    @staticmethod
    def generate_otp():
        return f"{random.randint(100000, 999999)}"

    @staticmethod
    def can_resend_otp(otp_sent_at):
        if not otp_sent_at:
            return True
        return datetime.utcnow() - otp_sent_at > timedelta(minutes=5)

    @staticmethod
    def is_otp_valid(otp_sent_at):
        if not otp_sent_at:
            return False
        return datetime.utcnow() - otp_sent_at <= timedelta(minutes=5)
