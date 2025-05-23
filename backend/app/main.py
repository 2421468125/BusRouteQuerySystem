import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import uvicorn
import json
from backend.app.core import Database 
import backend.app.api as routes 
from fastapi import FastAPI

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(routes.bus_routes_router)
    app.include_router(routes.bus_stops_router)
    app.include_router(routes.nearby_units_router)
    # db = Database.get_instance()
    Port = 0
    Host = ""
    with open("backend/app/settings.json", "r",encoding="utf-8") as f:
        config = json.load(f)
        Port = config["ServerPort"] 
        Host = config["ServerHost"]
    uvicorn.run("backend.app.main:app", host=Host, port=Port, reload=True)