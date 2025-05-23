import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import uvicorn
import json
from backend.app.core import Database 
import backend.app.api as routes 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import bus_routes, bus_stops, nearby_units, route_stops

app = FastAPI(title="Bus Route Query System API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中，应该设置为特定的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(bus_routes.router, tags=["Bus Routes"])
app.include_router(bus_stops.router, tags=["Bus Stops"])
app.include_router(nearby_units.router, tags=["Nearby Units"])
app.include_router(route_stops.router, tags=["Route Stops"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Bus Route Query System API"}

if __name__ == "__main__":
    db = Database.get_instance()
    # from backend.app.api.bus_routes import *
    Port = 0
    Host = ""
    with open("backend/app/settings.json", "r",encoding="utf-8") as f:
        config = json.load(f)
        Port = config["ServerPort"] 
        Host = config["ServerHost"]
    uvicorn.run("backend.app.main:app", host=Host, port=Port, reload=True)