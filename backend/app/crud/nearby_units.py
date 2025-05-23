from backend.app.core.database import Database

def create_nearby_unit(unit_id, unit_name, contact_phone, latitude, longitude, nearby_stop_id, distance_to_stop):
    query = """
    INSERT INTO BusSystem.NearbyUnit (unit_id, unit_name, contact_phone, latitude, longitude, nearby_stop_id, distance_to_stop)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    params = (unit_id, unit_name, contact_phone, latitude, longitude, nearby_stop_id, distance_to_stop)
    Database.get_instance().execute_query(query, params)

def read_nearby_units():
    query = "SELECT * FROM BusSystem.NearbyUnit;"
    return Database.get_instance().read_query(query)

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
    SELECT * FROM BusSystem.NearbyUnit;
    WHERE unit_id = %s;
    """
    params = (unit_id,)
    return Database.get_instance().read_query(query,params)