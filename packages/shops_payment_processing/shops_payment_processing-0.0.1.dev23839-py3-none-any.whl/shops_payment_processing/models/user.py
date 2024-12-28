from pydantic import BaseModel


class UserModel(BaseModel):
    tg_id: int
    first_name: str | None = ""
    last_name: str | None = ""
    tg_language: str | None = ""
    username: str | None = None