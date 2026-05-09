from pydantic import BaseModel, validator
from typing import Optional

# Define the user model
class User(BaseModel):
    username: str
    password: str
    email: str

    @validator("username")
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError("Username must be between 3 and 20 characters long")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8 or len(v) > 50:
            raise ValueError("Password must be between 8 and 50 characters long")
        return v

    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v

# Define the team model
class Team(BaseModel):
    name: str
    description: str

    @validator("name")
    def validate_name(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError("Team name must be between 3 and 20 characters long")
        return v

    @validator("description")
    def validate_description(cls, v):
        if len(v) < 10 or len(v) > 200:
            raise ValueError("Team description must be between 10 and 200 characters long")
        return v

# Define the file model
class File(BaseModel):
    file_name: str
    file_type: str

    @validator("file_name")
    def validate_file_name(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError("File name must be between 3 and 50 characters long")
        return v

    @validator("file_type")
    def validate_file_type(cls, v):
        if v not in ["image/jpeg", "image/png", "application/pdf"]:
            raise ValueError("Invalid file type")
        return v