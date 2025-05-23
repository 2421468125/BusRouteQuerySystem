<template>
  <div class="data-view">
    <h3>公交线路信息</h3>

    <div class="search-bar">
      <InputText
        v-model="searchName"
        type="text"
        placeholder="按名称查询"
        @keyup.enter="searchByName"
      />
      <Button icon="pi pi-search" label="搜索" @click="searchByName" />
    </div>

    <DataTable
      :value="paginatedBusRoutes"
      :loading="loading"
      class="p-datatable-gridlines"
      responsiveLayout="scroll"
      selectionMode="single"
      @row-click="showRouteDetails"
    >
      <Column field="routeNumber" header="线路编号"></Column>
      <Column field="routeName" header="线路名称"></Column>
      <Column field="mileage" header="运行里程 (km)"></Column>
      <Column field="firstDeparture" header="首班车时间"></Column>
      <Column field="lastDeparture" header="末班车时间"></Column>
      <Column field="peakInterval" header="高峰间隔 (min)"></Column>
      <Column field="offPeakInterval" header="平时间隔 (min)"></Column>
      <Column field="startStation" header="始发站点"></Column>
      <Column field="endStation" header="终点站点"></Column>
      <template #empty>
        <div class="p-text-center">没有找到公交线路数据。</div>
      </template>
      <template #loading>
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        正在加载公交线路数据...
      </template>
    </DataTable>

    <Paginator
      v-model:first="first"
      :rows="rows"
      :totalRecords="busRoutes.length"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      @page="onPageChange"
    />

    <Dialog
      v-model:visible="displayDialog"
      modal
      :header="
        selectedRoute ? selectedRoute.routeName + ' 线路详情' : '线路详情'
      "
      :style="{ width: '60vw' }"
      :breakpoints="{ '1199px': '80vw', '575px': '95vw' }"
      :closable="true"
    >
      <RouteDetailsDialog
        :routeNumber="selectedRoute ? selectedRoute.routeNumber : null"
      />
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Paginator from "primevue/paginator";
import apiManager from "@/services/api";

import RouteDetailsDialog from "./RouteDetailsDialog.vue";

const busRoutes = ref([]);
const loading = ref(true);
const searchName = ref("");

const displayDialog = ref(false);
const selectedRoute = ref(null); // 依然保留，用于显示弹框标题

// 分页相关参数
const first = ref(0);
const rows = ref(10);

// 计算当前页面数据
const paginatedBusRoutes = computed(() => {
  return busRoutes.value.slice(first.value, first.value + rows.value);
});

// 页面改变事件处理
const onPageChange = (event) => {
  first.value = event.first;
  rows.value = event.rows;
};

const fetchBusRoutes = async (name = "") => {
  loading.value = true;
  try {
    const response = await apiManager.getAllRoutes(name);
    let responseObject = responseAdapter(response).sort((a, b) =>
      a.routeNumber.localeCompare(b.routeNumber)
    );
    busRoutes.value = responseObject;
    first.value = 0; // 重置到第一页
  } catch (error) {
    console.error("获取公交线路数据失败:", error);
    busRoutes.value = [];
  } finally {
    loading.value = false;
  }
};

const searchByName = () => {
  fetchBusRoutes(searchName.value);
};

const showRouteDetails = (event) => {
  selectedRoute.value = event.data; // 存储选中行数据，用于弹框标题
  displayDialog.value = true; // 显示弹框
};

const responseAdapter = (response) => {
  if (!Array.isArray(response) || !response.every(Array.isArray)) {
    console.warn("API 响应格式不符合预期，期望二维数组。", response);
    return [];
  }
  return response
    .map((route) => {
      return {
        routeNumber: route[0],
        routeName: route[1],
        mileage: route[2],
        firstDeparture: route[3],
        lastDeparture: route[4],
        peakInterval: route[5],
        offPeakInterval: route[6],
        startStation: route[7] + route[9],
        endStation: route[8] + route[10],
      };
    })
    .filter(Boolean);
};

onMounted(() => {
  fetchBusRoutes();
});
</script>

<style lang="scss" scoped>
.data-view {
  padding: 1rem;
}
.search-bar {
  margin-bottom: 1rem;
  display: flex;
  gap: 0.5rem;
  .p-inputtext {
    flex: 1;
  }
}
</style>
