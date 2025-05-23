<template>
  <div class="data-view">
    <h3>公交站点信息</h3>

    <div class="search-bar">
      <InputText
        v-model="searchName"
        type="text"
        placeholder="按站点名称查询"
        @keyup.enter="searchByName"
      />
      <Button icon="pi pi-search" label="搜索" @click="searchByName" />
    </div>

    <DataTable
      :value="paginatedBusStops"
      :loading="loading"
      class="p-datatable-gridlines"
      responsiveLayout="scroll"
      selectionMode="single"
      @row-click="showStopDetails"
    >
      <Column field="stopId" header="站点编号"></Column>
      <Column field="stopName" header="站点名称"></Column>
      <Column field="latitude" header="纬度"></Column>
      <Column field="longitude" header="经度"></Column>
      <template #empty>
        <div class="p-text-center">没有找到公交站点数据。</div>
      </template>
      <template #loading>
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        正在加载公交站点数据...
      </template>
    </DataTable>

    <Paginator
      v-model:first="first"
      :rows="rows"
      :totalRecords="busStops.length"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      @page="onPageChange"
    />

    <Dialog
      v-model:visible="displayDialog"
      modal
      :header="selectedStop ? selectedStop.stopName + ' 站点详情' : '站点详情'"
      :style="{ width: '60vw' }"
      :breakpoints="{ '1199px': '80vw', '575px': '95vw' }"
      :closable="true"
    >
      <StopDetailsDialog :stopId="selectedStop ? selectedStop.stopId : null" />
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

import StopDetailsDialog from "./StopDetailsDialog.vue";

const busStops = ref([]);
const loading = ref(true);
const searchName = ref("");

const displayDialog = ref(false);
const selectedStop = ref(null);

// 分页相关参数
const first = ref(0);
const rows = ref(10);

// 计算当前页面数据
const paginatedBusStops = computed(() => {
  return busStops.value.slice(first.value, first.value + rows.value);
});

// 页面改变事件处理
const onPageChange = (event) => {
  first.value = event.first;
  rows.value = event.rows;
};

const fetchBusStops = async (name = "") => {
  loading.value = true;
  try {
    const response = await apiManager.getAllStops(name);
    let responseObject = responseAdapter(response).sort((a, b) =>
      a.stopId.localeCompare(b.stopId)
    );
    busStops.value = responseObject;
    first.value = 0; // 重置到第一页
  } catch (error) {
    console.error("获取公交站点数据失败:", error);
    busStops.value = [];
  } finally {
    loading.value = false;
  }
};

const searchByName = () => {
  fetchBusStops(searchName.value);
};

const showStopDetails = (event) => {
  selectedStop.value = event.data;
  displayDialog.value = true;
};

const responseAdapter = (response) => {
  if (!Array.isArray(response) || !response.every(Array.isArray)) {
    console.warn("API 响应格式不符合预期，期望二维数组。", response);
    return [];
  }
  return response
    .map((stop) => {
      return {
        stopId: stop[0],
        stopName: stop[1],
        latitude: stop[2],
        longitude: stop[3],
      };
    })
    .filter(Boolean);
};

onMounted(() => {
  fetchBusStops();
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
