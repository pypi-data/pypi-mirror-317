from pydantic import BaseModel, Field
from uuid import uuid4
from enum import Enum
from typing import List, Optional, Dict

class Roles(str, Enum):
    ADMIN = "admin"
    USER= "user"

class TenantMember(BaseModel):
    id: str = Field(description="User ID")
    roles: List[Roles] = Field(description="User roles", default=[Roles.USER], min_length=1)

class UserInfo(BaseModel):
    id: str = Field(description="User ID", default_factory=lambda: str(uuid4()))
    username: str = Field(description="Username")
    firstname: str = Field(description="First Name")
    lastname: str = Field(description="Last Name")
    email: str = Field(description="Email")
    roles:List[Roles] = Field(description="User roles", default=[Roles.USER],min_length=1)

class LoginData(BaseModel):
    username: str = Field(description="Username")
    password: str = Field(description="Password")

class ResetPasswordData(BaseModel):
    email: str = Field(description="Email")

class FinishResetPasswordData(BaseModel):
    token: str = Field(description="Reset token")
    password: str = Field(description="New password")

class RegisterData(BaseModel):
    firstname: str = Field(description="First Name",min_length=1)
    lastname: str = Field(description="Last Name",min_length=1)
    email: str = Field(description="Email",min_length=1)

class FinishRegistrationData(BaseModel):
    token: str = Field(description="Verification token")
    username: str = Field(description="Username")
    password: str = Field(description="Password")
    questions: Dict[str, str] = Field(description="Background questions")