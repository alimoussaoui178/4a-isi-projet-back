from pydantic import BaseModel, Field


class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=30)


class RegisterOut(BaseModel):
    id: int
    username: str
    password: str


class LoginIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    is_blocked: bool
    created_at: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class PasswordChangeIn(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)


class BlockIn(BaseModel):
    blocked: bool
