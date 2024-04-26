import re
from pydantic import BaseModel, validator
from validate_docbr import CPF  # type: ignore


class SubscriberDTO(BaseModel):
    name: str
    cpf: str
    email: str
    workload: float
    event_id: int

    @validator("cpf")
    def validate_cpf(cls, value: str):
        cpf_validator = CPF()

        if not cpf_validator.validate(value):
            raise ValueError("Invalid CPF")

        return value

    @validator("email")
    def validate_email(cls, value: str):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

        if not re.fullmatch(regex, value):
            raise ValueError("Invalid Email")

        return value
