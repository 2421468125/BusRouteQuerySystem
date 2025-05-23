from fastapi import APIRouter, Query, Body, HTTPException
from backend.app.crud.nearby_units import (
    read_nearby_units, 
    search_nearby_unit_details,
    create_nearby_unit,
    update_nearby_unit,
    delete_nearby_unit
)
from typing import Optional

router = APIRouter()

@router.get("/nearby_units")
def get_all_nearby_units(name: str = Query(None), nearby_stop_id: str = Query(None), skip: int = 0, limit: int = 100):
    return read_nearby_units(name=name, nearby_stop_id=nearby_stop_id, skip=skip, limit=limit)

@router.get("/nearby_units/{unit_id}")
def get_nearby_unit_details(unit_id: str):
    return search_nearby_unit_details(unit_id)

@router.post("/nearby_units")
def add_nearby_unit(
    unit_id: str = Body(...),
    unit_name: str = Body(...),
    contact_phone: Optional[str] = Body(None),
    latitude: Optional[float] = Body(None),
    longitude: Optional[float] = Body(None),
    nearby_stop_id: Optional[str] = Body(None),
    distance_to_stop: Optional[float] = Body(None)
):
    try:
        create_nearby_unit(
            unit_id, unit_name, contact_phone, latitude, longitude, 
            nearby_stop_id, distance_to_stop
        )
        return {"message": "Nearby unit created successfully", "unit_id": unit_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/nearby_units/{unit_id}")
def update_unit(
    unit_id: str,
    unit_name: Optional[str] = Body(None),
    contact_phone: Optional[str] = Body(None),
    latitude: Optional[float] = Body(None),
    longitude: Optional[float] = Body(None),
    nearby_stop_id: Optional[str] = Body(None),
    distance_to_stop: Optional[float] = Body(None)
):
    update_data = {}
    if unit_name is not None:
        update_data["unit_name"] = unit_name
    if contact_phone is not None:
        update_data["contact_phone"] = contact_phone
    if latitude is not None:
        update_data["latitude"] = latitude
    if longitude is not None:
        update_data["longitude"] = longitude
    if nearby_stop_id is not None:
        update_data["nearby_stop_id"] = nearby_stop_id
    if distance_to_stop is not None:
        update_data["distance_to_stop"] = distance_to_stop
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    try:
        update_nearby_unit(unit_id, **update_data)
        return {"message": "Nearby unit updated successfully", "unit_id": unit_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/nearby_units/{unit_id}")
def remove_nearby_unit(unit_id: str):
    try:
        delete_nearby_unit(unit_id)
        return {"message": "Nearby unit deleted successfully", "unit_id": unit_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))