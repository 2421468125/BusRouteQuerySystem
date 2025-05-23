CREATE SCHEMA IF NOT EXISTS BusSystem;
SET search_path TO BusSystem;

-- 公交线路表
CREATE TABLE IF NOT EXISTS BusSystem.BusRoute (
    route_id VARCHAR(50) PRIMARY KEY,
    route_name VARCHAR(100) NOT NULL,
    mileage DECIMAL(10, 2), -- 公交线路里程 (公里)
    first_bus_time TIME,
    last_bus_time TIME,
    peak_interval INT,     -- 高峰间隔分钟
    off_peak_interval INT, -- 平时间隔分钟
    start_station VARCHAR(20), -- 首末站
    end_station VARCHAR(20) -- 首末站
);

-- 公交站点表
CREATE TABLE IF NOT EXISTS BusSystem.BusStop (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 6),  -- 地理坐标纬度
    longitude DECIMAL(10, 6)  -- 地理坐标经度
);

-- 沿线单位表
CREATE TABLE IF NOT EXISTS BusSystem.NearbyUnit (
    unit_id VARCHAR(50) PRIMARY KEY,
    unit_name VARCHAR(200) NOT NULL,
    contact_phone VARCHAR(20),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    -- 与公交站点的临近关系
    nearby_stop_id VARCHAR(50),
    distance_to_stop DECIMAL(10, 2), -- 单位与临近站点的距离
    FOREIGN KEY (nearby_stop_id) REFERENCES BusStop(stop_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 线路停靠站点详情表 (多对多关系及顺序、距离、时间信息)
CREATE TABLE IF NOT EXISTS BusSystem.RouteStopDetail (
    route_id VARCHAR(50),
    stop_id VARCHAR(50),
    stop_order INT NOT NULL,           -- 停靠顺序
    distance_to_next_stop DECIMAL(10, 2), -- 到下一站的距离 (如果存在)
    avg_travel_time DECIMAL(10, 2),    -- 到下一站的平均运行时间 (分钟)
    PRIMARY KEY (route_id, stop_id),
    FOREIGN KEY (route_id) REFERENCES BusRoute(route_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES BusStop(stop_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 添加唯一性约束和索引以优化查询
CREATE UNIQUE INDEX IF NOT EXISTS idx_route_stop_order ON BusSystem.RouteStopDetail (route_id, stop_order);
CREATE INDEX IF NOT EXISTS idx_stop_name ON BusSystem.BusStop (stop_name);
CREATE INDEX IF NOT EXISTS idx_unit_name ON BusSystem.NearbyUnit (unit_name);