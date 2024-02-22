import re
from pydantic import BaseModel, validator


class UserDTO(BaseModel):
    email: str
    password: str

    @validator("password")
    def validate_password(cls, value: str):
        regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"

        if not re.match(regex, value):
            raise ValueError(
                "The password must contain at least 8 characters, one uppercase letter, one lowercase letter and one number"
            )

        return value

    @validator("email")
    def validate_email(cls, value: str):
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(regex, value):
            raise ValueError("Invalid email address")

        return value


class UserLoginDTO(BaseModel):
    username: str
    password: str
