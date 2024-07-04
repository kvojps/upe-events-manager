from pydantic import BaseModel


class PutObjectResponse(BaseModel):
    key_filename: str
