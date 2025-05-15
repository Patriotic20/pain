from pydantic import BaseModel , field_validator
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    password: str

    @field_validator("password" , mode="before")
    @classmethod
    def hash_password(cls , password):
        return pwd_context.hash(password)




class UserResponse(UserBase):
    id: int
    