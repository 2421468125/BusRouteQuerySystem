from backend.app.core.database import Database

def create_bus_route(route_id, route_name, mileage, first_bus_time, last_bus_time, peak_interval, off_peak_interval, start_station, end_station):
    query = """
    INSERT INTO BusSystem.BusRoute (route_id, route_name, mileage, first_bus_time, last_bus_time, peak_interval, off_peak_interval, start_station, end_station)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    params = (route_id, route_name, mileage, first_bus_time, last_bus_time, peak_interval, off_peak_interval, start_station, end_station)
    Database.get_instance().execute_query(query, params)

def read_bus_routes():
    query = "SELECT * FROM BusSystem.BusRoute;"
    return Database.get_instance().read_query(query)

def update_bus_route(route_id, **kwargs):
    updates = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    query = f"""
    UPDATE BusSystem.BusRoute
    SET {updates}
    WHERE route_id = %s;
    """
    params = (*kwargs.values(), route_id)
    Database.get_instance().execute_query(query, params)

def delete_bus_route(route_id):
    query = "DELETE FROM BusSystem.BusRoute WHERE route_id = %s;"
    params = (route_id,)
    Database.get_instance().execute_query(query, params)

def search_bus_routes_by_name(name, skip=0, limit=100):
    query = """
    SELECT * FROM BusSystem.BusRoute
    WHERE route_name LIKE %s
    LIMIT %s OFFSET %s;
    """
    params = (f"%{name}%", limit, skip)
    return Database.get_instance().read_query(query, params)

def search_bus_routes_by_stops(start_stop_name=None, end_stop_name=None):
    conditions = []
    params = []
    if start_stop_name:
        conditions.append("start_station LIKE %s")
        params.append(f"%{start_stop_name}%")
    if end_stop_name:
        conditions.append("end_station LIKE %s")
        params.append(f"%{end_stop_name}%")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    query = f"""
    SELECT * FROM BusSystem.BusRoute
    WHERE {where_clause};
    """
    return Database.get_instance().read_query(query, params)

def search_route_details_by_id(route_id: str):
    # 查询公交线路的基本信息
    route_query = """
    SELECT route_id, route_name, mileage, first_bus_time, last_bus_time, 
           peak_interval, off_peak_interval, start_station, end_station
    FROM BusSystem.BusRoute
    WHERE route_id = %s;
    """
    route_params = (route_id,)
    route_details = Database.get_instance().read_query(route_query, route_params)

    if not route_details:
        return None  # 如果线路不存在，返回 None

    # 查询公交线路的停靠站点信息
    stops_query = """
    SELECT stop_id, stop_name, latitude, longitude, stop_order, 
           distance_to_next_stop, avg_travel_time
    FROM BusSystem.BusStops
    WHERE route_id = %s
    ORDER BY stop_order ASC;
    """
    stops_params = (route_id,)
    stops_details = Database.get_instance().read_query(stops_query, stops_params)

    # 构造响应数据
    route_info = route_details[0]  # 假设 route_id 是唯一的
    return {
        "route_id": route_info["route_id"],
        "route_name": route_info["route_name"],
        "mileage": route_info["mileage"],
        "first_bus_time": route_info["first_bus_time"],
        "last_bus_time": route_info["last_bus_time"],
        "peak_interval": route_info["peak_interval"],
        "off_peak_interval": route_info["off_peak_interval"],
        "start_station": route_info["start_station"],
        "end_station": route_info["end_station"],
        "stops": stops_details
    }