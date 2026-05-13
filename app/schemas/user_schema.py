from pydantic import BaseModel, ConfigDict, EmailStr

from app.utils.security import hash_pass, verify_pass
from app.models.user import UserRole

class UserSignup(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole

    def hashed_password(self):
        return hash_pass(self.password)


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    token: str
    user: UserResponse