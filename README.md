## 使用方法：

- 根据本机配置修改 backend/app/settings.json 中的配置

```shell
cd backend && pip install -r requirements.txt

cd ../frontend && npm install

npm run both
```

# 公交线路查询系统项目报告

## 项目概述

公交线路查询系统是一个全栈应用程序，用于管理和查询城市公交线路、站点及相关信息。系统包括公交线路管理、站点管理、线路站点关系管理以及附近单位管理等功能。系统采用前后端分离架构，前端使用 Vue.js，后端使用 FastAPI，数据库使用 OpenGauss。

## 系统架构

### 项目结构

![structure.md](./structure.md)

### 技术栈

#### 前端

- **Vue.js 3**: 使用组合式 API 和 `<script setup>` 语法
- **PrimeVue**: UI 组件库
- **Axios**: HTTP 客户端

#### 后端

- **FastAPI**: Python Web 框架
- **OpenGauss**: 关系型数据库
- **Python**: 后端开发语言

## 数据模型

系统包含以下主要数据模型：

1. **BusRoute（公交线路）**

   - route_id: 线路编号
   - route_name: 线路名称
   - mileage: 里程
   - first_bus_time: 首班车时间
   - last_bus_time: 末班车时间
   - peak_interval: 高峰时段发车间隔
   - off_peak_interval: 平峰时段发车间隔
   - start_station: 起始站
   - end_station: 终点站

2. **BusStop（公交站点）**

   - stop_id: 站点编号
   - stop_name: 站点名称
   - latitude: 纬度
   - longitude: 经度

3. **RouteStopDetail（线路-站点关系）**

   - route_id: 线路编号
   - stop_id: 站点编号
   - stop_order: 站点顺序
   - distance_to_next_stop: 到下一站距离
   - avg_travel_time: 平均行程时间

4. **NearbyUnit（附近单位）**
   - nearby_stop_id: 邻近站点 ID
   - unit_name: 单位名称
   - contact_phone: 联系电话
   - latitude: 纬度
   - longitude: 经度
   - distance_to_stop: 到站点距离

## 功能模块

### 1. 公交线路管理

- 查看所有公交线路
- 添加、编辑、删除线路
- 查看线路详情（包括路线信息、站点信息、附近单位）

### 2. 公交站点管理

- 查看所有公交站点
- 添加、编辑、删除站点
- 查看站点详情（包括经过的线路、附近单位）

### 3. 线路站点关系管理

- 为线路添加/删除站点
- 编辑站点在线路中的顺序
- 编辑站点之间的距离和行程时间
- 通过拖拽重新排序站点

### 4. 附近单位管理

- 查看站点附近的单位
- 添加、编辑、删除附近单位

## API 接口

系统提供了以下主要 API 接口：

### 线路相关接口

- `GET /routes`: 获取所有线路
- `GET /routes/{route_id}`: 获取线路详情
- `POST /routes`: 添加新线路
- `PUT /routes/{route_id}`: 更新线路
- `DELETE /routes/{route_id}`: 删除线路

### 站点相关接口

- `GET /stops`: 获取所有站点
- `GET /stops/{stop_id}`: 获取站点详情
- `POST /stops`: 添加新站点
- `PUT /stops/{stop_id}`: 更新站点
- `DELETE /stops/{stop_id}`: 删除站点

### 线路-站点关系接口

- `GET /route_stops/{route_id}`: 获取线路的所有站点
- `POST /route_stops/{route_id}/stops`: 添加站点到线路
- `PUT /route_stops/{route_id}/stops/{stop_id}`: 更新线路站点信息
- `DELETE /route_stops/{route_id}/stops/{stop_id}`: 从线路中删除站点
- `POST /route_stops/{route_id}/reorder`: 重新排序站点

### 附近单位接口

- `GET /nearby_units`: 获取所有附近单位
- `GET /nearby_units/{unit_id}`: 获取单位详情
- `POST /nearby_units`: 添加新单位
- `PUT /nearby_units/{unit_id}`: 更新单位信息
- `DELETE /nearby_units/{unit_id}`: 删除单位

## 前端组件

系统包含以下主要前端组件：

1. **BusRoutes**: 显示所有公交线路
2. **BusRouteModify**: 管理公交线路
3. **BusStops**: 显示所有站点
4. **BusStopsModify**: 管理站点
5. **RouteStationModify**: 管理线路站点关系
6. **RouteDetailsDialog**: 显示线路详情
7. **StopDetailsDialog**: 显示站点详情
