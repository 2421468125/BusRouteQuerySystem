from fastapi import APIRouter, Query
from backend.app.crud.nearby_units import read_nearby_units, search_nearby_unit_details

router = APIRouter()

@router.get("/nearby_units")
def get_all_nearby_units(name: str = Query(None), nearby_stop_id: str = Query(None), skip: int = 0, limit: int = 100):
    # 假设 read_nearby_units 支持筛选参数
    return read_nearby_units(name=name, nearby_stop_id=nearby_stop_id, skip=skip, limit=limit)

@router.get("/nearby_units/{unit_id}")
def get_nearby_unit_details(unit_id: str):
    return search_nearby_unit_details(unit_id)