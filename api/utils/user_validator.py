import re
from validate_docbr import CPF  # type: ignore


def validate_cpf(cpf_validator: CPF, cpf: str) -> None:
    if not cpf_validator.validate(cpf):
        raise ValueError(f"Invalid CPF: {cpf}")


def validate_email(email: str) -> None:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    if not re.fullmatch(regex, email):
        raise ValueError(f"Invalid Email: {email}")
