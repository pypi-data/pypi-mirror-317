from datetime import datetime

from pydantic import BaseModel


class Credentails(BaseModel):
    access_token: str
    refresh_token: str
    login: str
    password: str
    access_until: datetime
    service_name: str
    created_at: datetime
