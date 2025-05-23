<template>
  <div class="data-view">
    <h3>附近单位信息</h3>

    <div class="search-bar">
      <InputText
        v-model="searchName"
        type="text"
        placeholder="按单位名称查询"
        @keyup.enter="searchByName"
      />
      <InputText
        v-model="searchStopId"
        type="text"
        placeholder="按附近站点ID查询"
        @keyup.enter="searchByName"
      />
      <Button icon="pi pi-search" label="搜索" @click="searchByName" />
    </div>

    <DataTable
      :value="paginatedNearbyUnits"
      :loading="loading"
      class="p-datatable-gridlines"
      responsiveLayout="scroll"
    >
      <Column field="unitId" header="单位编号"></Column>
      <Column field="unitName" header="单位名称"></Column>
      <Column field="contactPhone" header="联系电话"></Column>
      <Column field="nearbyStopId" header="附近站点ID"></Column>
      <Column field="distanceToStop" header="距离站点(km)"></Column>
      <template #empty>
        <div class="p-text-center">没有找到附近单位数据。</div>
      </template>
      <template #loading>
        <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        正在加载附近单位数据...
      </template>
    </DataTable>

    <Paginator
      v-model:first="first"
      :rows="rows"
      :totalRecords="nearbyUnits.length"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      @page="onPageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Paginator from "primevue/paginator";
import apiManager from "@/services/api";

const nearbyUnits = ref([]);
const loading = ref(true);
const searchName = ref("");
const searchStopId = ref("");

// 分页相关参数
const first = ref(0);
const rows = ref(10);

// 计算当前页面数据
const paginatedNearbyUnits = computed(() => {
  return nearbyUnits.value.slice(first.value, first.value + rows.value);
});

// 页面改变事件处理
const onPageChange = (event) => {
  first.value = event.first;
  rows.value = event.rows;
};

const fetchNearbyUnits = async (name = "", stopId = "") => {
  loading.value = true;
  try {
    const response = await apiManager.getNearbyUnits(
      name || null,
      stopId || null
    );
    nearbyUnits.value = responseAdapter(response).sort((a, b) =>
      a.unitId.localeCompare(b.unitId)
    );
    first.value = 0; // 重置到第一页
  } catch (error) {
    console.error("获取附近单位数据失败:", error);
    nearbyUnits.value = [];
  } finally {
    loading.value = false;
  }
};

const searchByName = () => {
  fetchNearbyUnits(searchName.value, searchStopId.value);
};

const responseAdapter = (response) => {
  if (!Array.isArray(response) || !response.every(Array.isArray)) {
    console.warn("API 响应格式不符合预期，期望二维数组。", response);
    return [];
  }
  return response
    .map((unit) => {
      return {
        unitId: unit[0],
        unitName: unit[1],
        contactPhone: unit[2],
        latitude: unit[3],
        longitude: unit[4],
        nearbyStopId: unit[5],
        distanceToStop: unit[6],
      };
    })
    .filter(Boolean);
};

onMounted(() => {
  fetchNearbyUnits();
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
