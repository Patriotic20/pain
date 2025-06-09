from passlib.context import CryptContext
from pydantic import BaseModel, field_validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(BaseModel):
    username: str
    password: str

    # @field_validator("password", mode="before")
    # @classmethod
    # def hash_password(cls, password):
    #     return pwd_context.hash(password)




class UserCreate(UserBase):
    role: str
    

class UserResponse(BaseModel):
    id: int
    username: str
    


