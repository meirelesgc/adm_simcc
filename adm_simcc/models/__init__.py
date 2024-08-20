from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class UserModel(BaseModel):
    displayName: str
    email: EmailStr
    uid: str
    photoURL: HttpUrl
    shib_id: Optional[str] = None
    linkedin: Optional[str] = None
    provider: Optional[str] = None
    lattes_id: Optional[str] = None
