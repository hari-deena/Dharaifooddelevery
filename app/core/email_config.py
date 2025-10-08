# import os
# from fastapi_mail import ConnectionConfig
# from pydantic import BaseModel, EmailStr
# from dotenv import load_dotenv
# from ..core.logger_config import configure_logger

# logger = configure_logger()


# # Load environment variables from .env file
# ENV_FILE = os.getenv('ENV_FILE', '.env.dev')
# load_dotenv(ENV_FILE)

# # This Pydantic model defines the required fields and types for email configuration settings
# class EmailSettings(BaseModel):
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_FROM: EmailStr
#     MAIL_PORT: int
#     MAIL_SERVER: str
#     MAIL_STARTTLS: bool
#     MAIL_SSL_TLS: bool

# # This line initializes the EmailSettings model by loading email configuration values from environment variables
# email_settings = EmailSettings(
#     MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
#     MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
#     MAIL_FROM=os.getenv('MAIL_FROM'),
#     MAIL_PORT=os.getenv('MAIL_PORT'),
#     MAIL_SERVER=os.getenv('MAIL_SERVER'),
#     MAIL_STARTTLS=os.getenv('MAIL_STARTTLS'),
#     MAIL_SSL_TLS=os.getenv('MAIL_SSL_TLS')
# )

# # This line creates the email ConnectionConfig using the validated settings from the EmailSettings 
# # model to enable sending emails.
# conf = ConnectionConfig(
#     MAIL_USERNAME=email_settings.MAIL_USERNAME,
#     MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
#     MAIL_FROM=email_settings.MAIL_FROM,
#     MAIL_PORT=email_settings.MAIL_PORT,
#     MAIL_SERVER=email_settings.MAIL_SERVER,
#     MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
#     MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
#     USE_CREDENTIALS=True
# )
