from fastapi import APIRouter, Query, Body, HTTPException
from backend.app.crud.route_stops import (
    add_stop_to_route,
    get_route_stops,
    update_route_stop,
    remove_stop_from_route,
    get_stops_on_route,
    get_routes_passing_stop,
    reorder_stops
)
from typing import Optional, List, Dict, Any

router = APIRouter()

@router.get("/route_stops/{route_id}")
def get_stops_for_route(route_id: str):
    """获取特定线路的所有站点"""
    try:
        stops = get_route_stops(route_id)
        return stops
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/route_stops/{route_id}/stops")
def add_stop_to_bus_route(
    route_id: str,
    stop_id: str = Body(...),
    stop_order: int = Body(...),
    distance_to_next_stop: Optional[float] = Body(None),
    avg_travel_time: Optional[float] = Body(None)
):
    """将站点添加到公交线路"""
    try:
        add_stop_to_route(
            route_id, stop_id, stop_order, 
            distance_to_next_stop, avg_travel_time
        )
        return {"message": "Stop added to route successfully", "route_id": route_id, "stop_id": stop_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/route_stops/{route_id}/stops/{stop_id}")
def update_stop_on_route(
    route_id: str,
    stop_id: str,
    stop_order: Optional[int] = Body(None),
    distance_to_next_stop: Optional[float] = Body(None),
    avg_travel_time: Optional[float] = Body(None)
):
    """更新线路上的站点信息"""
    update_data = {}
    if stop_order is not None:
        update_data["stop_order"] = stop_order
    if distance_to_next_stop is not None:
        update_data["distance_to_next_stop"] = distance_to_next_stop
    if avg_travel_time is not None:
        update_data["avg_travel_time"] = avg_travel_time
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    try:
        update_route_stop(route_id, stop_id, **update_data)
        return {"message": "Stop on route updated successfully", "route_id": route_id, "stop_id": stop_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/route_stops/{route_id}/stops/{stop_id}")
def delete_stop_from_route(route_id: str, stop_id: str):
    """从线路中删除站点"""
    try:
        remove_stop_from_route(route_id, stop_id)
        return {"message": "Stop removed from route successfully", "route_id": route_id, "stop_id": stop_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stop_routes/{stop_id}")
def get_routes_for_stop(stop_id: str):
    """获取经过特定站点的所有线路"""
    try:
        routes = get_routes_passing_stop(stop_id)
        return routes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/route_stops/{route_id}/reorder")
def reorder_stops_on_route(
    route_id: str,
    stop_ordering: List[Dict[str, Any]] = Body(...)
):
    """重新排序线路上的站点
    
    示例请求体:
    [
        {"stop_id": "S001", "stop_order": 1},
        {"stop_id": "S002", "stop_order": 2},
        {"stop_id": "S003", "stop_order": 3}
    ]
    """
    try:
        reorder_stops(route_id, stop_ordering)
        return {"message": "Stops reordered successfully", "route_id": route_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))