from fastapi import APIRouter, Query, Body, HTTPException
from backend.app.crud.bus_routes import (
    search_bus_routes_by_name,
    search_route_details_by_id,
    create_bus_route,
    update_bus_route,
    delete_bus_route,
    read_bus_routes
)
from typing import Optional

router = APIRouter()


@router.get("/routes")
def get_all_routes(name: str = Query(None), skip: int = 0, limit: int = 100):
    print("get_all_routes", name, skip, limit)
    if name:
        return search_bus_routes_by_name(name, skip, limit)
    return search_bus_routes_by_name("", skip, limit)


@router.get("/routes/{route_id}")
def get_route_details(route_id: str):
    return search_route_details_by_id(route_id)

@router.post("/routes")
def add_route(
    route_id: str = Body(...),
    route_name: str = Body(...),
    mileage: Optional[float] = Body(None),
    first_bus_time: Optional[str] = Body(None),
    last_bus_time: Optional[str] = Body(None),
    peak_interval: Optional[int] = Body(None),
    off_peak_interval: Optional[int] = Body(None),
    start_station: Optional[str] = Body(None),
    end_station: Optional[str] = Body(None)
):
    try:
        create_bus_route(
            route_id, route_name, mileage, first_bus_time, last_bus_time,
            peak_interval, off_peak_interval, start_station, end_station
        )
        return {"message": "Bus route created successfully", "route_id": route_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/routes/{route_id}")
def update_route(
    route_id: str,
    route_name: Optional[str] = Body(None),
    mileage: Optional[float] = Body(None),
    first_bus_time: Optional[str] = Body(None),
    last_bus_time: Optional[str] = Body(None),
    peak_interval: Optional[int] = Body(None),
    off_peak_interval: Optional[int] = Body(None),
    start_station: Optional[str] = Body(None),
    end_station: Optional[str] = Body(None)
):
    update_data = {}
    if route_name is not None:
        update_data["route_name"] = route_name
    if mileage is not None:
        update_data["mileage"] = mileage
    if first_bus_time is not None:
        update_data["first_bus_time"] = first_bus_time
    if last_bus_time is not None:
        update_data["last_bus_time"] = last_bus_time
    if peak_interval is not None:
        update_data["peak_interval"] = peak_interval
    if off_peak_interval is not None:
        update_data["off_peak_interval"] = off_peak_interval
    if start_station is not None:
        update_data["start_station"] = start_station
    if end_station is not None:
        update_data["end_station"] = end_station
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    try:
        update_bus_route(route_id, **update_data)
        return {"message": "Bus route updated successfully", "route_id": route_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/routes/{route_id}")
def remove_route(route_id: str):
    try:
        delete_bus_route(route_id)
        return {"message": "Bus route deleted successfully", "route_id": route_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


