from fastapi import FastAPI
from app.routes.endpoints import router
from app.routes.websocket import ws_router

app = FastAPI()
app.include_router(router)
app.include_router(ws_router)
