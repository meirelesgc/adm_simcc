from pydantic import BaseModel, EmailStr, HttpUrl


class UserModel(BaseModel):
    displayName: str
    email: EmailStr
    uid: str
    photoURL: HttpUrl
