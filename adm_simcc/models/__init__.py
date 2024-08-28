from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class UserModel(BaseModel):
    displayName: str
    email: EmailStr
    uid: str = None
    photoURL: Optional[HttpUrl] = None
    shib_id: Optional[str] = None
    shib_code: Optional[str] = None
    linkedin: Optional[str] = None
    provider: Optional[str] = None
    lattes_id: Optional[str] = None
