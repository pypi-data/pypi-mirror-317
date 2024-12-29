from pydantic import BaseModel


class UserAuth(BaseModel):
    school_code: str
