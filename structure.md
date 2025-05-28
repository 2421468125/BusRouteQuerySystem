BusRouteQuerySystem/
├── frontend/
│ ├── public/
│ │ └── favicon.ico
│ ├── src/
│ │ ├── assets/ # 静态资源，如图片、样式
│ │ │ └── main.css
│ │ ├── components/ # 可复用组件
│ │ ├── views/ # 页面级组件
│ │ ├── router/
│ │ │ └── index.js # Vue Router 配置
│ │ ├── services/
│ │ │ ├── axios.js # axios 设置
│ │ │ └── api.js # API 请求封装
│ │ ├── App.vue # 根组件
│ │ └── main.js # Vue 应用入口
│ ├── index.html # HTML 模板
│ ├── package.json # Node.js 依赖及脚本
│ └── vite.config.js # Vite 配置
|
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ ├── **init**.py
│ │ │ ├── bus_routes.py # 公交线路相关 API
│ │ │ ├── bus_stops.py # 公交站点相关 API
│ │ │ └── nearby_units.py # 沿线单位相关 API
│ │ ├── crud/
│ │ │ ├── **init**.py
│ │ │ ├── bus_routes.py # 公交线路数据操作
│ │ │ ├── bus_stops.py # 公交站点数据操作
│ │ │ └── nearby_units.py # 沿线单位数据操作
│ │ ├── core/
│ │ │ ├── **init**.py
│ │ │ └── database.py # 数据库连接和会话管理
| | ├── settings.json # 后端与数据库参数
│ │ └── main.py # FastAPI 应用入口
│ ├── tests/ # 后端测试文件 (可选)
│ │ └── test_api.py
│ ├── .env.example # 环境变量示例文件
│ └── requirements.txt # Python 依赖
|
├── database/
│ ├── init_db.sql # 数据库初始化脚本（创建表、索引等）
│ └── insert_data.sql
