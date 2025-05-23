from fastapi import APIRouter, Query, Body, HTTPException
from backend.app.crud.bus_stops import (
    search_bus_stops_by_name, 
    get_bus_stop_details,
    create_bus_stop,
    update_bus_stop,
    delete_bus_stop,
    read_bus_stops
)
from typing import Optional

router = APIRouter()

@router.get("/stops")
def get_all_stops(name: str = Query(None), skip: int = 0, limit: int = 100):
    if name:
        return search_bus_stops_by_name(name, skip, limit)
    return search_bus_stops_by_name("", skip, limit)

@router.get("/stops/{stop_id}")
def get_stop_details(stop_id: str):
    return get_bus_stop_details(stop_id)

@router.post("/stops")
def add_stop(
    stop_id: str = Body(...),
    stop_name: str = Body(...),
    latitude: Optional[float] = Body(None),
    longitude: Optional[float] = Body(None)
):
    try:
        create_bus_stop(stop_id, stop_name, latitude, longitude)
        return {"message": "Bus stop created successfully", "stop_id": stop_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/stops/{stop_id}")
def update_stop(
    stop_id: str,
    stop_name: Optional[str] = Body(None),
    latitude: Optional[float] = Body(None),
    longitude: Optional[float] = Body(None)
):
    update_data = {}
    if stop_name is not None:
        update_data["stop_name"] = stop_name
    if latitude is not None:
        update_data["latitude"] = latitude
    if longitude is not None:
        update_data["longitude"] = longitude
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    try:
        update_bus_stop(stop_id, **update_data)
        return {"message": "Bus stop updated successfully", "stop_id": stop_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/stops/{stop_id}")
def remove_stop(stop_id: str):
    try:
        delete_bus_stop(stop_id)
        return {"message": "Bus stop deleted successfully", "stop_id": stop_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))