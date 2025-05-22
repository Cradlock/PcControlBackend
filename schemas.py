from pydantic import BaseModel


class user_data(BaseModel):
    username : str 
    password : str


class RegisterData(BaseModel):
    username: str
    password: str
    secret_key: str


