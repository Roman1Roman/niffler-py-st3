from pydantic import BaseModel

class Envs(BaseModel):
    auth_url: str
    frontend_url: str
    gateway_url: str
    spends_db_url: str
    test_username: str
    test_password: str