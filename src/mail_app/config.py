import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List



load_dotenv()

HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = os.environ.get("MAIL_PORT", 465)


class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str