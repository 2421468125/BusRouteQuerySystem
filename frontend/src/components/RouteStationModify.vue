<template>
  <div class="route-station-modify">
    <div class="route-selection-panel">
      <h2>线路站点关系管理</h2>
      <div class="p-field route-selector">
        <label for="route-selector">选择线路</label>
        <Dropdown
          id="route-selector"
          v-model="selectedRoute"
          :options="routes"
          optionLabel="name"
          placeholder="请选择线路"
          :filter="true"
          :loading="routesLoading"
          @change="loadRouteStops"
        />
      </div>
    </div>

    <div v-if="selectedRoute" class="stops-panel">
      <div class="stops-header">
        <h3>{{ selectedRoute.name }} 的站点列表</h3>
        <div class="stops-actions">
          <Button
            label="添加站点"
            icon="pi pi-plus"
            @click="openAddStopDialog"
          />
          <Button
            label="保存排序"
            icon="pi pi-save"
            class="p-button-success p-ml-2"
            @click="saveStopOrder"
            :disabled="!stopsChanged"
          />
        </div>
      </div>

      <DataTable
        v-model:selection="selectedStops"
        :value="routeStops"
        responsiveLayout="scroll"
        class="p-datatable-sm"
        :loading="stopsLoading"
        @row-reorder="onRowReorder"
        reorderableRows
        stripedRows
        dataKey="stop_id"
      >
        <Column :rowReorder="true" style="width: 3rem" />
        <Column field="stop_number" header="站点序号" sortable></Column>
        <Column field="stop_id" header="站点编号"></Column>
        <Column field="stop_name" header="站点名称"></Column>
        <Column field="distance_to_next_stop" header="下站距离(km)"></Column>
        <Column field="avg_travel_time" header="平均耗时(min)"></Column>
        <Column header="操作">
          <template #body="slotProps">
            <Button
              label="改"
              icon="pi pi-pencil"
              class="p-button-rounded p-button-success p-button-sm p-mr-2"
              @click="editRouteStop(slotProps.data)"
            />
            <Button
              label="删"
              icon="pi pi-trash"
              class="p-button-rounded p-button-danger p-button-sm"
              @click="confirmDeleteRouteStop(slotProps.data)"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <div v-else class="empty-state">
      <div class="empty-message">
        <i class="pi pi-info-circle" style="font-size: 2rem"></i>
        <p>请先选择一条线路</p>
      </div>
    </div>

    <!-- 添加站点到线路对话框 -->
    <Dialog
      v-model:visible="addStopDialog"
      :style="{ width: '500px' }"
      header="添加站点到线路"
      :modal="true"
      class="p-fluid"
    >
      <div class="p-field">
        <label for="stop_id">选择站点</label>
        <Dropdown
          id="stop_id"
          v-model="routeStop.stop_id"
          :options="availableStops"
          optionLabel="name"
          optionValue="_id"
          placeholder="选择站点"
          :filter="true"
          :class="{ 'p-invalid': submitted && !routeStop.stop_id }"
        />
        <small class="p-error" v-if="submitted && !routeStop.stop_id"
          >站点必选</small
        >
      </div>
      <div class="p-field">
        <label for="stop_number">站点序号</label>
        <InputNumber
          id="stop_number"
          v-model="routeStop.stop_number"
          :min="1"
          :max="999"
          :class="{ 'p-invalid': submitted && !routeStop.stop_number }"
        />
        <small class="p-error" v-if="submitted && !routeStop.stop_number"
          >站点序号必填</small
        >
      </div>
      <div class="p-field">
        <label for="distance_to_next_stop">下站距离(km)</label>
        <InputText
          id="distance_to_next_stop"
          v-model="routeStop.distance_to_next_stop"
          type="number"
        />
      </div>
      <div class="p-field">
        <label for="avg_travel_time">平均耗时(min)</label>
        <InputText
          id="avg_travel_time"
          v-model="routeStop.avg_travel_time"
          type="number"
        />
      </div>
      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="hideAddStopDialog"
        />
        <Button
          label="保存"
          icon="pi pi-check"
          class="p-button-text"
          @click="saveRouteStop"
        />
      </template>
    </Dialog>

    <!-- 编辑线路站点对话框 -->
    <Dialog
      v-model:visible="editStopDialog"
      :style="{ width: '500px' }"
      header="编辑线路站点"
      :modal="true"
      class="p-fluid"
    >
      <div class="p-field">
        <label for="edit_stop_name">站点名称</label>
        <InputText
          id="edit_stop_name"
          v-model.trim="routeStop.stop_name"
          disabled
        />
      </div>
      <div class="p-field">
        <label for="edit_stop_number">站点序号</label>
        <InputNumber
          id="edit_stop_number"
          v-model="routeStop.stop_number"
          :min="1"
          :max="999"
          :class="{ 'p-invalid': submitted && !routeStop.stop_number }"
        />
        <small class="p-error" v-if="submitted && !routeStop.stop_number"
          >站点序号必填</small
        >
      </div>
      <div class="p-field">
        <label for="distance_to_next_stop">下站距离(km)</label>
        <InputText
          id="distance_to_next_stop"
          v-model.trim="routeStop.distance_to_next_stop"
          type="number"
        />
      </div>
      <div class="p-field">
        <label for="avg_travel_time">平均耗时(min)</label>
        <InputText
          id="avg_travel_time"
          v-model.trim="routeStop.avg_travel_time"
          type="number"
        />
      </div>

      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="editStopDialog = false"
        />
        <Button
          label="保存"
          icon="pi pi-check"
          class="p-button-text"
          @click="updateRouteStop"
        />
      </template>
    </Dialog>

    <!-- 删除确认框 -->
    <Dialog
      v-model:visible="deleteStopDialog"
      :style="{ width: '450px' }"
      header="确认删除"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
        <span v-if="routeStop"
          >确定要从线路 <b>{{ selectedRoute?.name }}</b> 中删除站点
          <b>{{ routeStop.stop_name }}</b> 吗？</span
        >
      </div>
      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="deleteStopDialog = false"
        />
        <Button
          label="确认删除"
          icon="pi pi-check"
          class="p-button-text p-button-danger"
          @click="deleteRouteStop"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Dropdown from "primevue/dropdown";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Textarea from "primevue/textarea";
import { useToast } from "primevue/usetoast";
import apiManager from "@/services/api";

const toast = useToast();
const routes = ref([]);
const routesLoading = ref(false);
const selectedRoute = ref(null);
const routeStops = ref([]);
const stopsLoading = ref(false);
const allStops = ref([]);
const addStopDialog = ref(false);
const editStopDialog = ref(false);
const deleteStopDialog = ref(false);
const routeStop = ref({});
const submitted = ref(false);
const selectedStops = ref([]);
const originalStopsOrder = ref([]);
const stopsChanged = ref(false);

// 计算可用于添加到线路的站点（排除已添加的）
const availableStops = computed(() => {
  if (!allStops.value || !routeStops.value) return [];

  // 获取已添加到线路的站点ID列表
  const addedStopIds = routeStops.value.map((rs) => rs.stop_id);

  // 过滤出未添加的站点
  return allStops.value.filter((stop) => !addedStopIds.includes(stop._id));
});

// 加载所有线路
const loadRoutes = async () => {
  routesLoading.value = true;
  try {
    const response = await apiManager.getAllRoutes();
    routes.value = response.map((route) => {
      return {
        _id: route[0],
        name: route[1],
        routeNumber: route[0],
        routeName: route[1],
        mileage: route[2],
        firstDeparture: route[3],
        lastDeparture: route[4],
        peakInterval: route[5],
        offPeakInterval: route[6],
        startStation: route[7],
        endStation: route[8],
      };
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "加载失败",
      detail: "无法获取线路数据",
      life: 3000,
    });
    console.error("获取线路数据失败:", error);
  } finally {
    routesLoading.value = false;
  }
};

// 加载所有站点
const loadAllStops = async () => {
  try {
    const response = await apiManager.getAllStops();
    allStops.value = response.map((stop) => {
      return {
        _id: stop[0],
        name: stop[1],
        latitude: stop[2],
        longitude: stop[3],
      };
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "加载失败",
      detail: "无法获取站点数据",
      life: 3000,
    });
    console.error("获取站点数据失败:", error);
  }
};

// 加载线路的站点
const loadRouteStops = async () => {
  if (!selectedRoute.value) return;

  stopsLoading.value = true;
  try {
    const response = await apiManager.getStopsForRoute(selectedRoute.value._id);
    routeStops.value = response.map((stop) => {
      return {
        stop_id: stop[1],
        stop_name: stop[2],
        stop_number: stop[3],
        distance_to_next_stop: stop[4],
        avg_travel_time: stop[5],
      };
    });
    // 存储原始排序，用于检测变化
    originalStopsOrder.value = [
      ...routeStops.value.map((stop) => ({
        stop_id: stop.stop_id,
        stop_order: stop.stop_number,
      })),
    ];
    stopsChanged.value = false;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "加载失败",
      detail: "无法获取线路站点数据",
      life: 3000,
    });
    console.error("获取线路站点数据失败:", error);
  } finally {
    stopsLoading.value = false;
  }
};

// 行重新排序处理
const onRowReorder = (event) => {
  stopsChanged.value = true;
  // 更新站点序号
  routeStops.value.forEach((stop, index) => {
    stop.stop_number = index + 1;
  });
};

// 打开添加站点对话框
const openAddStopDialog = () => {
  routeStop.value = {
    stop_id: null,
    stop_number: routeStops.value.length + 1,
  };
  submitted.value = false;
  addStopDialog.value = true;
};

// 隐藏添加站点对话框
const hideAddStopDialog = () => {
  addStopDialog.value = false;
  submitted.value = false;
};

// 保存站点到线路
const saveRouteStop = async () => {
  submitted.value = true;

  if (!routeStop.value.stop_id || !routeStop.value.stop_number) {
    return;
  }

  try {
    stopsLoading.value = true;
    await apiManager.addStopToRoute(selectedRoute.value._id, {
      stop_id: routeStop.value.stop_id,
      stop_order: routeStop.value.stop_number,
      avg_travel_time: routeStop.value.avg_travel_time,
      distance_to_next_stop: routeStop.value.distance_to_next_stop,
    });
    addStopDialog.value = false;
    await loadRouteStops();
    toast.add({
      severity: "success",
      summary: "操作成功",
      detail: "站点已添加到线路",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: "添加站点到线路失败",
      life: 3000,
    });
    console.error("添加站点到线路失败:", error);
  } finally {
    stopsLoading.value = false;
  }
};

// 打开编辑线路站点对话框
const editRouteStop = (data) => {
  routeStop.value = { ...data };
  editStopDialog.value = true;
  submitted.value = false;
};

// 更新线路站点
const updateRouteStop = async () => {
  submitted.value = true;

  if (!routeStop.value.stop_number) {
    return;
  }

  try {
    stopsLoading.value = true;
    await apiManager.updateStopOnRoute(
      selectedRoute.value._id,
      routeStop.value.stop_id,
      {
        stop_order: routeStop.value.stop_number,
        distance_to_next_stop: routeStop.value.distance_to_next_stop,
        avg_travel_time: routeStop.value.avg_travel_time,
      }
    );
    editStopDialog.value = false;
    await loadRouteStops();
    toast.add({
      severity: "success",
      summary: "操作成功",
      detail: "线路站点已更新",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: "更新线路站点失败",
      life: 3000,
    });
    console.error("更新线路站点失败:", error);
  } finally {
    stopsLoading.value = false;
  }
};

// 确认删除线路站点
const confirmDeleteRouteStop = (data) => {
  routeStop.value = data;
  deleteStopDialog.value = true;
};

// 删除线路站点
const deleteRouteStop = async () => {
  try {
    stopsLoading.value = true;
    await apiManager.deleteStopFromRoute(
      selectedRoute.value._id,
      routeStop.value.stop_id
    );
    deleteStopDialog.value = false;
    await loadRouteStops();
    toast.add({
      severity: "success",
      summary: "操作成功",
      detail: "站点已从线路中删除",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: "从线路中删除站点失败",
      life: 3000,
    });
    console.error("从线路中删除站点失败:", error);
  } finally {
    stopsLoading.value = false;
  }
};

// 保存站点排序
const saveStopOrder = async () => {
  if (!stopsChanged.value) return;

  try {
    stopsLoading.value = true;

    // 准备排序数据
    const orderData = routeStops.value.map((stop) => ({
      stop_id: stop.stop_id,
      stop_order: stop.stop_number,
    }));

    await apiManager.reorderStopsOnRoute(selectedRoute.value._id, orderData);
    stopsChanged.value = false;
    toast.add({
      severity: "success",
      summary: "操作成功",
      detail: "站点排序已保存",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: "保存站点排序失败",
      life: 3000,
    });
    console.error("保存站点排序失败:", error);
  } finally {
    stopsLoading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadRoutes();
  loadAllStops();
});
</script>

<style lang="scss" scoped>
.route-station-modify {
  .route-selection-panel {
    display: flex;
    flex-direction: column;
    margin-bottom: 1.5rem;

    h2 {
      margin-top: 0;
      margin-bottom: 1rem;
    }

    .route-selector {
      width: 100%;
      max-width: 500px;
    }
  }

  .stops-panel {
    .stops-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;

      h3 {
        margin: 0;
      }

      .stops-actions {
        display: flex;
        gap: 0.5rem;
      }
    }
  }

  .empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
    background-color: #f8f9fa;
    border-radius: 8px;

    .empty-message {
      text-align: center;
      color: #6c757d;

      i {
        display: block;
        margin-bottom: 1rem;
      }

      p {
        font-size: 1.1rem;
        margin: 0;
      }
    }
  }

  .p-field {
    margin-bottom: 1.5rem;
  }

  .confirmation-content {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 0;
  }
}
</style>
