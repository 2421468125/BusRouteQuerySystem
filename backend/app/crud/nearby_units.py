from backend.app.core.database import Database

def create_nearby_unit(unit_id, unit_name, contact_phone, latitude, longitude, nearby_stop_id, distance_to_stop):
    query = """
    INSERT INTO BusSystem.NearbyUnit (unit_id, unit_name, contact_phone, latitude, longitude, nearby_stop_id, distance_to_stop)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    params = (unit_id, unit_name, contact_phone, latitude, longitude, nearby_stop_id, distance_to_stop)
    Database.get_instance().execute_query(query, params)

def read_nearby_units(name=None, nearby_stop_id=None, skip=0, limit=100):
    base_query = "SELECT * FROM BusSystem.NearbyUnit"
    conditions = []
    params = []
    
    if name:
        conditions.append("unit_name LIKE %s")
        params.append(f"%{name}%")
    
    if nearby_stop_id:
        conditions.append("nearby_stop_id = %s")
        params.append(nearby_stop_id)
    
    if conditions:
        query = f"{base_query} WHERE {' AND '.join(conditions)}"
    else:
        query = base_query
    
    query += f" LIMIT {skip}, {limit}"
    
    return Database.get_instance().read_query(query, params if params else None)

def update_nearby_unit(unit_id, **kwargs):
    updates = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    query = f"""
    UPDATE BusSystem.NearbyUnit
    SET {updates}
    WHERE unit_id = %s;
    """
    params = (*kwargs.values(), unit_id)
    Database.get_instance().execute_query(query, params)

def delete_nearby_unit(unit_id):
    query = "DELETE FROM BusSystem.NearbyUnit WHERE unit_id = %s;"
    params = (unit_id,)
    Database.get_instance().execute_query(query, params)

def search_nearby_unit_details(unit_id):
    query = """
    SELECT * FROM BusSystem.NearbyUnit
    WHERE unit_id = %s;
    """
    params = (unit_id,)
    return Database.get_instance().read_query(query, params)