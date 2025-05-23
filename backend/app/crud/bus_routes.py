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
    SELECT 
        br.route_id, 
        br.route_name, 
        br.mileage, 
        br.first_bus_time, 
        br.last_bus_time, 
        br.peak_interval, 
        br.off_peak_interval, 
        br.start_station, 
        br.end_station, 
        ss1.stop_name AS start_station_name, 
        ss2.stop_name AS end_station_name
    FROM 
        BusSystem.BusRoute br
    LEFT JOIN 
        BusSystem.BusStop ss1 ON br.start_station = ss1.stop_id
    LEFT JOIN 
        BusSystem.BusStop ss2 ON br.end_station = ss2.stop_id
    WHERE route_name LIKE %s
    LIMIT %s OFFSET %s;
    """
    params = (f"%{name}%", limit, skip)
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
    SELECT rsd.stop_id, bs.stop_name, bs.latitude, bs.longitude, rsd.stop_order, 
           rsd.distance_to_next_stop, rsd.avg_travel_time
    FROM BusSystem.RouteStopDetail rsd
    JOIN BusSystem.BusStop bs ON rsd.stop_id = bs.stop_id
    WHERE rsd.route_id = %s
    ORDER BY rsd.stop_order ASC;
    """
    stops_params = (route_id,)
    stops_details = Database.get_instance().read_query(stops_query, stops_params)

    # 查询每个站台的附近单位信息
    nearby_units_query = """
    SELECT nearby_stop_id, unit_name, contact_phone, latitude, longitude, distance_to_stop
    FROM BusSystem.NearbyUnit
    WHERE nearby_stop_id IN (SELECT stop_id FROM BusSystem.RouteStopDetail WHERE route_id = %s);
    """
    nearby_units_params = (route_id,)
    nearby_units_details = Database.get_instance().read_query(nearby_units_query, nearby_units_params)
    # 构造响应数据
    route_info = route_details[0]  # 假设 route_id 是唯一的
    return {
        "route_id": route_info[0],
        "route_name": route_info[1],
        "mileage": route_info[2],
        "first_bus_time": route_info[3],
        "last_bus_time": route_info[4],
        "peak_interval": route_info[5],
        "off_peak_interval": route_info[6],
        "start_station": route_info[7],
        "end_station": route_info[8],
        "stops": stops_details,
        "nearby_units": nearby_units_details
    }