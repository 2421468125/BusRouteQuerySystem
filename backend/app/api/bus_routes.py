from fastapi import APIRouter, Query
from backend.app.crud.bus_routes import (
    search_bus_routes_by_name,
    search_bus_routes_by_stops,
    search_route_details_by_id,
)

router = APIRouter()


@router.get("/routes")
def get_all_routes(name: str = Query(None), skip: int = 0, limit: int = 100):
    if name:
        return search_bus_routes_by_name(name, skip, limit)
    return search_bus_routes_by_name("", skip, limit)


@router.get("/routes/{route_id}")
def get_route_details(route_id: str):
    return search_route_details_by_id(route_id)


@router.get("/routes/search_by_stops")
def search_routes_by_stops(
    start_stop_name: str = Query(None), end_stop_name: str = Query(None)
):
    return search_bus_routes_by_stops(start_stop_name, end_stop_name)

