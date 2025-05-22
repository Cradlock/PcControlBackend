from fastapi import FastAPI,WebSocket,WebSocketDisconnect,Response,Cookie,Form,File,UploadFile
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import settings
import json
import base64
from db import *
from utils import *
from schemas import *
import psycopg2.errors as db_error



app = FastAPI()

session : Session 

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)

# pc-Name    -    WebSocket 
connected_pc = {}
# session_id   -   user_id
sessions = {}

Secret_key = "SKY"


@app.get("/")
def main():
   text = ""
   with open("index.html","r") as f:
      text = f.read()
   return HTMLResponse(content=text,status_code=200)


@app.websocket("/openC")
async def chat_pces(websocket: WebSocket):
    await websocket.accept()
    try:
     while True:
        message = await websocket.receive_text()
        data = json.loads(message)

        pc_name = data["name"]
        key = data["key"]
        if key == settings.shift_string(pc_name):
            print(f'Connected {pc_name}   ---key {key}')
            await websocket.send_text("OK")
            connected_pc[pc_name] = websocket
            print(connected_pc)
        else:
            await websocket.close()
    except WebSocketDisconnect:
       print("Client disconnect")


@app.get("/list_connected_pc")
async def connected_pc(session_id : str = Cookie(None)):
   if sessions.get(session_id) is None:
      return JSONResponse(content="Error",status_code=403)
   
   return JSONResponse(content={"connected_pc":list(connected_pc.keys())})


@app.post("/login")
async def login(res : Response,post_data : user_data,session: Session = Depends(get_session)):
   username = post_data.username
   password = post_data.password

   user = User.getUser(session=session,username=username,password=password )
   if user == 404:
      return JSONResponse(content={"data":"User not found"},status_code=404)
   if user == 403:
      return JSONResponse(content={"data":"Incorrect password"},status_code=403)
   
   token = generate_key()
   sessions[token] = user.id
   res.set_cookie(key="token",value=token)
   return JSONResponse(content={
      "username":user.username
   },status_code=200)


@app.post("/register")
async def register(res : Response,data : RegisterData):
   username = data.username
   password = data.password
   secret_key = data.secret_key

   if secret_key != Secret_key:
      return JSONResponse(content={"msg":"Incorrect word (idi nahyui chmo blyat) "},status_code=403)
   
   token = generate_key()

   try:
      user = User(username=username,password=hashed(password))
      session.add(user)
      session.commit()
   except db_error.UniqueViolation as e:
      return JSONResponse(content={"msg":"This user has in db"},status_code=409)
   except Exception as e:
      print(e)
      return JSONResponse(content={"msg":"Error in db"},status_code=500)
   
   
   sessions[token] = user.id

   return JSONResponse(content=user,status_code=200)

   
@app.post("/logout")
async def logout(res : Response,session_id : str = Cookie(None)):
    if session_id:
       del sessions[session_id]
    else:
       return {"data":"You aren't authentication "}




@app.post("/sendCommand")
async def sendCommand(session_id : str = Cookie(None),command : str = Form(...),list_pc : List[str] = Form(...)):
   if sessions.get(session_id) is None:
      return JSONResponse(content={},status_code=403)
   success = []
   failed = []
   
   for name,wbsock in connected_pc.items():
      if name in list_pc:
         try:
             await wbsock.send_json({"type":"command","text":command})
             success.append(name)
         except Exception as e:
            print(f"error {e}")
            failed.append(name)

   return JSONResponse(content={
      "success":success,
      "failed":failed
   },status_code=200)


@app.post("/sendFile")
async def sendFile(session_id : str = Cookie(None),file : UploadFile = File(...),list_pc : List[str] = Form(...)):
   if sessions.get(session_id) is None:
      return JSONResponse(content={},status_code=403)
   
   content = await file.read()
   success = []
   failed = []
   for name,wbsock in connected_pc.items():
      if name in list_pc:
         try:
             await wbsock.send_json({"type":"file",
                                     "filename":file.filename,
                                     "data":  base64.b64encode(content).decode('utf-8') })
             success.append(name)
         except Exception as e:
            print(f"error {e}")
            failed.append(name)

   return JSONResponse(content={
      "success":success,
      "failed":failed
   },status_code=200)


def get_session():
    db = session
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    try:
         session = get_session()
         session.execute(text("SELECT 1"))
         print(session)
         if session is None:
           print("ERROR with db")
         else:
           print("DB Connected ")
    except Exception as e:
       print(f"Error {e}")