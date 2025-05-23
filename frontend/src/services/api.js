import service from "./axios";

// 获取所有公交线路
const getAllRoutes = async (name = null, skip = 0, limit = 100) => {
  console.log("getAllRoutes", name, skip, limit,__BASE_URL__);
  let params = name ? {name, skip, limit} : {skip, limit};
  return service.get("/routes", {
    params: params,
  });
};

// 根据线路 ID 获取公交线路详情
const getRouteDetails = async (routeId) => {
  return service.get(`/routes/${routeId}`);
};

// 添加公交线路
const addRoute = async (routeData) => {
  return service.post("/routes", routeData);
};

// 更新公交线路
const updateRoute = async (routeId, routeData) => {
  return service.put(`/routes/${routeId}`, routeData);
};

// 删除公交线路
const deleteRoute = async (routeId) => {
  return service.delete(`/routes/${routeId}`);
};

// 根据起点和终点站名搜索公交线路
const searchRoutesByStops = async (startStopName = "", endStopName = "") => {
  return service.get("/routes/search_by_stops", {
    params: { start_stop_name: startStopName, end_stop_name: endStopName },
  });
};

// 获取所有公交站点
const getAllStops = async (name = null, skip = 0, limit = 100) => {
  let params = name ? { name, skip, limit } : { skip, limit };
  return service.get("/stops", {
    params: params,
  });
};

// 获取站点详情
const getStopDetails = async (stopId) => {
  return service.get(`/stops/${stopId}`);
};

// 添加公交站点
const addStop = async (stopData) => {
  return service.post("/stops", stopData);
};

// 更新公交站点
const updateStop = async (stopId, stopData) => {
  return service.put(`/stops/${stopId}`, stopData);
};

// 删除公交站点
const deleteStop = async (stopId) => {
  return service.delete(`/stops/${stopId}`);
};

// 获取线路的所有站点
const getStopsForRoute = async (routeId) => {
  return service.get(`/route_stops/${routeId}`);
};

// 添加站点到线路
const addStopToRoute = async (routeId, stopData) => {
  return service.post(`/route_stops/${routeId}/stops`, stopData);
};

// 更新线路上的站点信息
const updateStopOnRoute = async (routeId, stopId, stopData) => {
  return service.put(`/route_stops/${routeId}/stops/${stopId}`, stopData);
};

// 从线路中删除站点
const deleteStopFromRoute = async (routeId, stopId) => {
  return service.delete(`/route_stops/${routeId}/stops/${stopId}`);
};

// 获取经过某站点的所有线路
const getRoutesForStop = async (stopId) => {
  return service.get(`/stop_routes/${stopId}`);
};

// 重新排序线路上的站点
const reorderStopsOnRoute = async (routeId, stopOrdering) => {
  return service.post(`/route_stops/${routeId}/reorder`, stopOrdering);
};

// 获取附近单位
const getNearbyUnits = async (name = null, nearbyStopId = null, skip = 0, limit = 100) => {
  let params = {};
  if (name) params.name = name;
  if (nearbyStopId) params.nearby_stop_id = nearbyStopId;
  params.skip = skip;
  params.limit = limit;
  
  return service.get("/nearby_units", {
    params: params,
  });
};

// 获取附近单位详情
const getNearbyUnitDetails = async (unitId) => {
  return service.get(`/nearby_units/${unitId}`);
};

// 添加附近单位
const addNearbyUnit = async (unitData) => {
  return service.post("/nearby_units", unitData);
};

// 更新附近单位
const updateNearbyUnit = async (unitId, unitData) => {
  return service.put(`/nearby_units/${unitId}`, unitData);
};

// 删除附近单位
const deleteNearbyUnit = async (unitId) => {
  return service.delete(`/nearby_units/${unitId}`);
};

const apiManager = {
  getAllRoutes,
  getRouteDetails,
  addRoute,
  updateRoute,
  deleteRoute,
  searchRoutesByStops,
  getAllStops,
  getStopDetails,
  addStop,
  updateStop,
  deleteStop,
  getStopsForRoute,
  addStopToRoute,
  updateStopOnRoute,
  deleteStopFromRoute,
  getRoutesForStop,
  reorderStopsOnRoute,
  getNearbyUnits,
  getNearbyUnitDetails,
  addNearbyUnit,
  updateNearbyUnit,
  deleteNearbyUnit,
}

export default apiManager;