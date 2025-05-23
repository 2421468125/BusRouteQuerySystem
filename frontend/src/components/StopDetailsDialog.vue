<template>
  <div class="stop-details-dialog-container">
    <div v-if="loading" class="p-text-center p-py-3">
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      正在加载站点详情...
    </div>
    <div v-else-if="error" class="p-message p-message-error">
      <div class="p-message-wrapper">
        <span class="p-message-icon pi pi-times-circle"></span>
        <div class="p-message-text">{{ error }}</div>
      </div>
    </div>
    <div v-else-if="stopDetails">
      <Tabs value="0">
        <TabList>
          <Tab value="0">站点基本信息</Tab>
          <Tab value="1">经过线路信息</Tab>
          <Tab value="2">附近单位信息</Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="0">
            <div class="p-fluid p-formgrid p-grid">
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>站点编号:</label>
                  <p>{{ stopDetails.stop_details[0][0] }}</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>站点名称:</label>
                  <p>{{ stopDetails.stop_details[0][1] }}</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>纬度:</label>
                  <p>{{ stopDetails.stop_details[0][2] }}</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>经度:</label>
                  <p>{{ stopDetails.stop_details[0][3] }}</p>
                </div>
              </div>
            </div>
          </TabPanel>

          <TabPanel value="1">
            <DataTable
              :value="passingRoutes"
              class="p-datatable-gridlines"
              responsiveLayout="scroll"
            >
              <Column field="routeId" header="线路编号"></Column>
              <Column field="routeName" header="线路名称"></Column>
              <Column field="startStation" header="始发站"></Column>
              <Column field="endStation" header="终点站"></Column>
              <Column field="stopOrder" header="站点顺序"></Column>
              <template #empty>
                <div class="p-text-center">该站点没有经过线路信息。</div>
              </template>
            </DataTable>
          </TabPanel>

          <TabPanel value="2">
            <DataTable
              :value="nearbyUnits"
              class="p-datatable-gridlines"
              responsiveLayout="scroll"
            >
              <Column field="unitName" header="单位名称"></Column>
              <Column field="contactPhone" header="联系电话"></Column>
              <Column field="latitude" header="纬度"></Column>
              <Column field="longitude" header="经度"></Column>
              <Column field="distanceToStop" header="距站点距离(km)"></Column>
              <template #empty>
                <div class="p-text-center">该站点没有附近单位信息。</div>
              </template>
            </DataTable>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
    <div v-else class="p-text-center p-py-3">未选择站点或无详情数据。</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { defineProps } from "vue";
import apiManager from "@/services/api";
import Tabs from "primevue/tabs";
import TabList from "primevue/tablist";
import Tab from "primevue/tab";
import TabPanels from "primevue/tabpanels";
import TabPanel from "primevue/tabpanel";
import DataTable from "primevue/datatable";
import Column from "primevue/column";

const props = defineProps({
  stopId: {
    type: String, // 站点编号，对应后端的 stop_id
    default: null,
  },
});

const stopDetails = ref(null);
const loading = ref(false);
const error = ref(null);

// 处理经过线路的数据
const passingRoutes = computed(() => {
  if (!stopDetails.value || !stopDetails.value.passing_routes) {
    return [];
  }
  return stopDetails.value.passing_routes.map((route) => ({
    routeId: route[0],
    routeName: route[1],
    startStation: route[2],
    endStation: route[3],
    stopOrder: route[4],
  }));
});

// 处理附近单位的数据
const nearbyUnits = computed(() => {
  if (!stopDetails.value || !stopDetails.value.nearby_units) {
    return [];
  }
  return stopDetails.value.nearby_units.map((unit) => ({
    unitName: unit[1],
    contactPhone: unit[2],
    latitude: unit[3],
    longitude: unit[4],
    distanceToStop: unit[5],
  }));
});

const fetchStopDetails = async (stopId) => {
  if (!stopId) {
    stopDetails.value = null;
    error.value = null;
    return;
  }

  loading.value = true;
  error.value = null;
  stopDetails.value = null; // 清空旧数据

  try {
    const data = await apiManager.getStopDetails(stopId);
    console.log("获取到的站点详情数据:", data);
    stopDetails.value = data;
    loading.value = false;
  } catch (err) {
    console.error("获取站点详情失败:", err);
    error.value = "加载站点详情失败，请稍后再试。";
    loading.value = false;
  }
};

// 首次挂载时加载数据
onMounted(() => {
  fetchStopDetails(props.stopId);
});

// 监听 stopId prop 的变化，重新加载数据
watch(
  () => props.stopId,
  (newVal) => {
    fetchStopDetails(newVal);
  }
);
</script>

<style lang="scss" scoped>
.stop-details-dialog-container {
  padding: 1rem;
}

.p-field {
  margin-bottom: 1rem;
  label {
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 0.25rem;
  }
  p {
    margin: 0;
    color: #555;
    font-size: 1.1rem;
  }
}

// PrimeVue DataTable 的一些自定义样式
.p-datatable-gridlines {
  .p-datatable-thead > tr > th {
    background-color: #f8f9fa;
    font-weight: bold;
  }
}
</style>
