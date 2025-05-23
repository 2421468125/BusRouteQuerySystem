from backend.app.core.database import Database

def add_stop_to_route(route_id, stop_id, stop_order, distance_to_next_stop=None, avg_travel_time=None):
    query = """
    INSERT INTO BusSystem.RouteStopDetail 
    (route_id, stop_id, stop_order, distance_to_next_stop, avg_travel_time)
    VALUES (%s, %s, %s, %s, %s);
    """
    params = (route_id, stop_id, stop_order, distance_to_next_stop, avg_travel_time)
    Database.get_instance().execute_query(query, params)

def get_route_stops(route_id):
    query = """
    SELECT rsd.route_id, rsd.stop_id, bs.stop_name, rsd.stop_order, 
           rsd.distance_to_next_stop, rsd.avg_travel_time
    FROM BusSystem.RouteStopDetail rsd
    JOIN BusSystem.BusStop bs ON rsd.stop_id = bs.stop_id
    WHERE rsd.route_id = %s
    ORDER BY rsd.stop_order ASC;
    """
    params = (route_id,)
    return Database.get_instance().read_query(query, params)

def update_route_stop(route_id, stop_id, **kwargs):
    updates = ", ".join([f"{key} = %s" for key in kwargs.keys()])
    query = f"""
    UPDATE BusSystem.RouteStopDetail
    SET {updates}
    WHERE route_id = %s AND stop_id = %s;
    """
    params = (*kwargs.values(), route_id, stop_id)
    Database.get_instance().execute_query(query, params)

def remove_stop_from_route(route_id, stop_id):
    query = """
    DELETE FROM BusSystem.RouteStopDetail 
    WHERE route_id = %s AND stop_id = %s;
    """
    params = (route_id, stop_id)
    Database.get_instance().execute_query(query, params)

def get_stops_on_route(route_id):
    query = """
    SELECT rsd.stop_id, bs.stop_name, rsd.stop_order, 
           rsd.distance_to_next_stop, rsd.avg_travel_time
    FROM BusSystem.RouteStopDetail rsd
    JOIN BusSystem.BusStop bs ON rsd.stop_id = bs.stop_id
    WHERE rsd.route_id = %s
    ORDER BY rsd.stop_order ASC;
    """
    params = (route_id,)
    return Database.get_instance().read_query(query, params)

def get_routes_passing_stop(stop_id):
    query = """
    SELECT rsd.route_id, br.route_name, rsd.stop_order
    FROM BusSystem.RouteStopDetail rsd
    JOIN BusSystem.BusRoute br ON rsd.route_id = br.route_id
    WHERE rsd.stop_id = %s
    ORDER BY rsd.route_id, rsd.stop_order;
    """
    params = (stop_id,)
    return Database.get_instance().read_query(query, params)

def reorder_stops(route_id, stop_ordering_data):
    """
    重新排序路线上的站点
    
    参数:
    - route_id: 路线ID
    - stop_ordering_data: 站点排序数据，格式为 [{stop_id: xxx, stop_order: n}, ...]
    """
    db = Database.get_instance()
    try:
        # 开始事务
        db.begin_transaction()
        
        for item in stop_ordering_data:
            query = """
            UPDATE BusSystem.RouteStopDetail
            SET stop_order = %s
            WHERE route_id = %s AND stop_id = %s;
            """
            params = (item['stop_order'], route_id, item['stop_id'])
            db.execute_query(query, params)
        
        # 提交事务
        db.commit_transaction()
        return True
    except Exception as e:
        # 回滚事务
        db.rollback_transaction()
        raise e