from pydantic import BaseModel


class ExceptionResponse(BaseModel):
    detail: str
