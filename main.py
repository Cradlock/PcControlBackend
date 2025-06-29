from fastapi import FastAPI,WebSocket,WebSocketDisconnect,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse,HTMLResponse
import init

app = FastAPI()

origins = [
    "http://localhost:3000",  # локальный фронт
    "https://it-log-9ukw.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # список разрешённых источников
    allow_credentials=True,  # можно передавать куки
    allow_methods=["*"],  # разрешить все методы: GET, POST и т.п.
    allow_headers=["*"], 
)

connected_pc = dict()

@app.websocket("/openC")
async def open_chat(websocket : WebSocket):
    await websocket.accept()
    name = None
    try:
        while True:
            data = await websocket.receive_json()
            name = data.get("name",None)
            if name:
                connected_pc[name] = websocket
                print(name)
                await websocket.send_text("OK")

    except WebSocketDisconnect:
        
        print("Client disconnect")
        if name and name in connected_pc:
            connected_pc.pop(name)
            print(f"{name}  -  removed in connected")





@app.get("/")
async def root():
    text = ""
    with open("index.html","r") as f:
        text = f.read()
    return HTMLResponse(text)




@app.get("/clients")
async def getClients(isAuth : bool = Depends(init.verify_token)):
    # if not isAuth:
        # return JSONResponse({"error":"Unathorizated"},status_code=401)
    return JSONResponse({"pc_names": list(connected_pc.keys()) })


@app.post("/sendCommand")
async def sendCommand(data : init.DataCommand,isAuth : bool = Depends(init.verify_token)):
    # if isAuth:
        try:
           success = []
           failed = []
           for name,ws in connected_pc.items():
              if name in data.recepients:
                try:
                    await ws.send_json(
                      {
                        "type":"command",
                        "text":data.command
                     }
                    )
                    success.append(name)
                except Exception:
                    failed.append(name)
        
           return {"success":success,"failed":failed}
        except Exception as e:
           print(e) 
           return JSONResponse({"msg":"Internal server error"},status_code=500)
    # else:
        # return JSONResponse({"error":"Not authorizited"},status_code=401)


@app.post("sendFile/")
async def sendFile(isAuth : bool = Depends(init.verify_token)):
    pass    








