
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os

template_env = Environment(loader=FileSystemLoader("app/template"))

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS", "True").lower() == "true"
)

async def send_email(email: str, otp: str):
    template = template_env.get_template("email_template.html")

    html_content = template.render(
        otp=otp,
        logo_url="https://img.favpng.com/1/9/24/car-motor-vehicle-steering-wheels-ship-s-wheel-png-favpng-uciUhnY6UbBgjSKt45Jpy9Gx7.jpg", 
        company_name="Ridelly",
        current_year=datetime.now().year,
        website_url="https://ridelly.com"
    )

    message = MessageSchema(
        subject="Verify Your Account - Ridelly",
        recipients=[email],
        body=html_content,
        subtype="html" 
    )

    fm = FastMail(conf)
    await fm.send_message(message)
