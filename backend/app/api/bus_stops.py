from fastapi import APIRouter, Query
from backend.app.crud.bus_stops import search_bus_stops_by_name, get_bus_stop_details

router = APIRouter()

@router.get("/stops")
def get_all_stops(name: str = Query(None), skip: int = 0, limit: int = 100):
    if name:
        return search_bus_stops_by_name(name, skip, limit)
    return search_bus_stops_by_name("", skip, limit)

@router.get("/stops/{stop_id}")
def get_stop_details(stop_id: str):
    return get_bus_stop_details(stop_id)