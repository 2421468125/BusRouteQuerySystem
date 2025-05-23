from backend.app.core.database import Database

def create_bus_stop(stop_id, stop_name, latitude, longitude):
    query = """
    INSERT INTO BusSystem.BusStop (stop_id, stop_name, latitude, longitude)
    VALUES (%s, %s, %s, %s);
    """
    params = (stop_id, stop_name, latitude, longitude)
    Database.get_instance().execute_query(query, params)

def read_bus_stops():
    query = "SELECT * FROM BusSystem.BusStop;"
    return Database.get_instance().read_query(query)

def update_bus_stop(stop_id, **kwargs):
    updates = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    query = f"""
    UPDATE BusSystem.BusStop
    SET {updates}
    WHERE stop_id = %s;
    """
    params = (*kwargs.values(), stop_id)
    Database.get_instance().execute_query(query, params)

def delete_bus_stop(stop_id):
    query = "DELETE FROM BusSystem.BusStop WHERE stop_id = %s;"
    params = (stop_id,)
    Database.get_instance().execute_query(query, params)

def search_bus_stops_by_name(name, skip=0, limit=100):
    query = """
    SELECT * FROM BusSystem.BusStop
    WHERE stop_name LIKE %s
    LIMIT %s OFFSET %s;
    """
    params = (f"%{name}%", limit, skip)
    return Database.get_instance().read_query(query, params)

def get_bus_stop_details(stop_id):
    query = """
    SELECT * FROM BusSystem.BusStop WHERE stop_id = %s;
    """
    stop_details = Database.get_instance().read_query(query, (stop_id,))

    nearby_units_query = """
    SELECT * FROM BusSystem.NearbyUnit WHERE nearby_stop_id = %s;
    """
    nearby_units = Database.get_instance().read_query(nearby_units_query, (stop_id,))

    passing_routes_query = """
    SELECT r.route_id, r.route_name, r.start_station, r.end_station, sr.stop_order
    FROM BusSystem.BusRoute r
    JOIN BusSystem.StopRoute sr ON r.route_id = sr.route_id
    WHERE sr.stop_id = %s;
    """
    passing_routes = Database.get_instance().read_query(passing_routes_query, (stop_id,))

    return {
        "stop_details": stop_details,
        "nearby_units": nearby_units,
        "passing_routes": passing_routes
    }