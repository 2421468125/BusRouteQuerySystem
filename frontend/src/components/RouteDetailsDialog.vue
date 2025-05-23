<template>
  <div class="route-details-dialog-container">
    <div v-if="loading" class="p-text-center p-py-3">
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      正在加载线路详情...
    </div>
    <div v-else-if="error" class="p-message p-message-error">
      <div class="p-message-wrapper">
        <span class="p-message-icon pi pi-times-circle"></span>
        <div class="p-message-text">{{ error }}</div>
      </div>
    </div>
    <div v-else-if="routeDetails">
      <Tabs value="0">
        <TabList>
          <Tab value="0">线路基本信息</Tab>
          <Tab value="1">停靠站点信息</Tab>
          <Tab value="2">沿线单位信息</Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="0">
            <div class="p-fluid p-formgrid p-grid">
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>线路编号:</label>
                  <p>{{ routeDetails.route_id }}</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>线路名称:</label>
                  <p>{{ routeDetails.route_name }}</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>运行里程:</label>
                  <p>{{ routeDetails.mileage }} km</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>首班车时间:</label>
                  <p>{{ routeDetails.first_bus_time }}</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>末班车时间:</label>
                  <p>{{ routeDetails.last_bus_time }}</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>高峰间隔:</label>
                  <p>{{ routeDetails.peak_interval }} 分钟</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>平时间隔:</label>
                  <p>{{ routeDetails.off_peak_interval }} 分钟</p>
                </div>
              </div>
              <div class="p-col-12 p-md-6">
                <div class="p-field">
                  <label>首末站点:</label>
                  <p>
                    {{ routeDetails.start_station }} -
                    {{ routeDetails.end_station }}
                  </p>
                </div>
              </div>
            </div>
          </TabPanel>

          <TabPanel value="1">
            <DataTable
              :value="routeDetails.stops"
              class="p-datatable-gridlines"
              responsiveLayout="scroll"
            >
              <Column field="stop_order" header="顺序"></Column>
              <Column field="stop_name" header="站点名称"></Column>
              <Column field="stop_id" header="站点编号"></Column>
              <Column field="latitude" header="纬度"></Column>
              <Column field="longitude" header="经度"></Column>
              <Column
                field="distance_to_next_stop"
                header="距下一站 (km)"
              ></Column>
              <Column field="avg_travel_time" header="平均耗时 (min)"></Column>
              <template #empty>
                <div class="p-text-center">该线路没有停靠站点信息。</div>
              </template>
            </DataTable>
          </TabPanel>

          <TabPanel value="2">
            <DataTable
              :value="routeDetails.nearby_units"
              class="p-datatable-gridlines"
              responsiveLayout="scroll"
            >
              <Column field="stopOrder" header="靠站顺序"></Column>
              <Column field="nearbyStop" header="站点名称"></Column>
              <Column field="unitName" header="单位名称"></Column>
              <Column field="contactPhone" header="站点编号"></Column>
              <Column field="latitude" header="纬度"></Column>
              <Column field="longitude" header="经度"></Column>
              <Column field="distanceToStop" header="距站点距离(km)"></Column>
              <template #empty>
                <div class="p-text-center">该线路没有沿线单位信息。</div>
              </template>
            </DataTable>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
    <div v-else class="p-text-center p-py-3">未选择线路或无详情数据。</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
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
  routeNumber: {
    type: String, // 线路编号，对应后端的 route_id
    default: null,
  },
});

const routeDetails = ref(null);
const loading = ref(false);
const error = ref(null);

const fetchRouteDetails = async (routeId) => {
  if (!routeId) {
    routeDetails.value = null;
    error.value = null;
    return;
  }

  loading.value = true;
  error.value = null;
  routeDetails.value = null; // 清空旧数据

  try {
    let data = await apiManager.getRouteDetails(routeId);
    console.log("获取到的线路详情数据:", data["nearby_units"]);
    data["stops"] = data["stops"].map((item) => ({
      stop_order: item[4],
      stop_name: item[1],
      stop_id: item[0],
      latitude: item[2],
      longitude: item[3],
      distance_to_next_stop: item[5],
      avg_travel_time: item[6],
    }));

    data["nearby_units"] = data["nearby_units"]
      .map((item) => {
        const stopInfo = findStopById(data["stops"], item[0]);
        return {
          stopOrder: stopInfo.stop_order,
          nearbyStop: stopInfo.stop_name,
          unitName: item[1],
          contactPhone: item[2],
          latitude: item[3],
          longitude: item[4],
          distanceToStop: item[5],
        };
      })
      .sort((a, b) => a.stopOrder - b.stopOrder);

    routeDetails.value = data;
    console.log("获取到的线路详情:", routeDetails.value);
    loading.value = false;
  } catch (err) {
    console.error("获取线路详情失败:", err);
    error.value = "加载线路详情失败，请稍后再试。";
  }
};

function findStopById(stops, stopId) {
  let result = null;
  stops.forEach((element) => {
    if (element.stop_id == stopId) {
      result = element;
    }
  });
  return result;
}

// 首次挂载时加载数据
onMounted(() => {
  fetchRouteDetails(props.routeNumber);
});

// 监听 routeNumber prop 的变化，重新加载数据
watch(
  () => props.routeNumber,
  (newVal) => {
    fetchRouteDetails(newVal);
  }
);
</script>

<style lang="scss" scoped>
.route-details-dialog-container {
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
