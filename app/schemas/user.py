from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

# 1. Base User Schema ( shared fields for many operations )
class UserBase(BaseModel):
    username: str = Field( min_length=3, max_length=50, examples=["Tom"])
    email: EmailStr = Field( examples=["max@example.com"])

# 2. SingUp Request model (Registration)
class UserSingUp(UserBase):
    password: str = Field(min_length=8, max_length=100, examples=["secret_password123"])

# 3. SingIn Request model ( Log in )
class UserSingIn(BaseModel):
    email: EmailStr = Field(examples=["max@exammle.com"])
    password: str = Field(examples=["secret_password123"])

# 4. UserUpdate Request model ( Profile update )
class UserUpdate(BaseModel):
    username: Optional [str] = Field(None, min_length=3, max_length=50, examples=["new_Tom"])
    email: Optional [EmailStr] = Field(None, examples=["new_email@example.com"])
    password: Optional [str] = Field(None, min_length=8, max_length=100)
    is_active: Optional[bool] = None

# 5. UserDetail Response ( Detail user information int the output )
class UserDetail(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        # This parameter allows Pydantic to automatically read data from SQLAlchemy (ORM)
        orm_mode= True

# 6. UserList Response (Returning a list of users with pagination)
class UserList(BaseModel):
    users: List[UserDetail]
    total: int

    class ConfigDict:
        orm_mode = True






