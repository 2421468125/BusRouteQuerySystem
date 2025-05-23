<template>
  <div class="data-view">
    <h3>公交线路信息</h3>
    <DataTable
      :value="busRoutes"
      :loading="loading"
      class="p-datatable-gridlines"
      responsiveLayout="scroll"
    >
      <Column field="routeNumber" header="线路编号"></Column>
      <Column field="routeName" header="线路名称"></Column>
      <Column field="mileage" header="运行里程 (km)"></Column>
      <Column field="firstDeparture" header="首班车时间"></Column>
      <Column field="lastDeparture" header="末班车时间"></Column>
      <Column field="peakInterval" header="高峰间隔 (min)"></Column>
      <Column field="normalInterval" header="平时间隔 (min)"></Column>
      <Column field="startEndStations" header="首末站点"></Column>
      <template #empty>
        <div class="p-text-center">没有找到公交线路数据。</div>
      </template>
      <template #loading>
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        正在加载公交线路数据...
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
// 引入 axios 或 fetch API 用于数据请求
import axios from "axios"; // 假设你已经安装了 axios

const busRoutes = ref([]);
const loading = ref(true); // 添加加载状态

// 模拟后端 API 地址
const API_URL = "/api/busroutes"; // 你需要替换成实际的后端API地址

const fetchBusRoutes = async () => {
  loading.value = true; // 开始加载
  try {
    const response = await axios.get(API_URL);
    busRoutes.value = response.data; // 假设后端返回的数据就是我们需要的数组
  } catch (error) {
    console.error("获取公交线路数据失败:", error);
    // 可以添加错误提示给用户
  } finally {
    loading.value = false; // 停止加载
  }
};

// 在组件挂载时调用数据获取函数
onMounted(() => {
  fetchBusRoutes();
});
</script>

<style lang="scss" scoped>
.data-view {
  padding: 1rem;
}
</style>
