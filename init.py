from fastapi import Cookie
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
import os
AUTH_KEY : str = "" 
API_HOST : str = ""


class DataCommand(BaseModel):
    recepients : List[str]
    command : str

def verify_token(auth_key : str  =  Cookie(None)) -> bool:
    if auth_key == AUTH_KEY:
        return True
    return False
        
    



if __name__ == "__main__":
    load_dotenv()
    AUTH_KEY = os.getenv("SECRET_KEY")
    API_HOST = os.getenv("HOST")
    print(AUTH_KEY,API_HOST)
