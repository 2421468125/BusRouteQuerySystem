<template>
  <div class="bus-route-modify">
    <div class="route-header">
      <h2>公交线路管理</h2>
      <Button label="添加线路" icon="pi pi-plus" @click="openNewRouteDialog" />
    </div>

    <DataTable
      :value="routes"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      responsiveLayout="scroll"
      class="p-datatable-sm"
      :loading="loading"
      v-model:filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['route_name', 'route_id']"
    >
      <template #header>
        <div class="table-header">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              placeholder="搜索线路..."
            />
          </span>
        </div>
      </template>

      <Column field="route_id" header="线路编号" sortable></Column>
      <Column field="route_name" header="线路名称" sortable></Column>
      <Column field="first_bus_time" header="首班时间"></Column>
      <Column field="last_bus_time" header="末班时间"></Column>
      <Column field="peak_interval" header="高峰间隔"></Column>
      <Column field="off_peak_interval" header="平时间隔"></Column>
      <Column field="mileage" header="里程" sortable></Column>
      <Column header="操作">
        <template #body="slotProps">
          <Button
            label="改"
            icon="pi pi-pencil"
            class="p-button-rounded p-button-success p-button-sm p-mr-2"
            @click="editRoute(slotProps.data)"
          />
          <Button
            label="删"
            icon="pi pi-trash"
            class="p-button-rounded p-button-danger p-button-sm"
            @click="confirmDeleteRoute(slotProps.data)"
          />
        </template>
      </Column>
    </DataTable>

    <!-- 添加/编辑线路对话框 -->
    <Dialog
      v-model:visible="routeDialog"
      :style="{ width: '500px' }"
      :header="editMode ? '编辑线路' : '添加线路'"
      :modal="true"
      class="p-fluid"
    >
      <div class="p-field">
        <label for="route_id">线路编号</label>
        <InputText
          id="route_id"
          v-model.trim="route.route_id"
          required="true"
          autofocus
          :class="{ 'p-invalid': submitted && !route.route_id }"
          :disabled="editMode"
        />
        <small class="p-error" v-if="submitted && !route.route_id"
          >线路编号必填</small
        >
      </div>
      <div class="p-field">
        <label for="route_name">线路名称</label>
        <InputText
          id="route_name"
          v-model.trim="route.route_name"
          required="true"
          :class="{ 'p-invalid': submitted && !route.route_name }"
        />
        <small class="p-error" v-if="submitted && !route.route_name"
          >线路名称必填</small
        >
      </div>
      <div class="p-field">
        <label for="first_bus_time">首班时间</label>
        <InputText id="first_bus_time" v-model.trim="route.first_bus_time" />
      </div>
      <div class="p-field">
        <label for="last_bus_time">末班时间</label>
        <InputText id="last_bus_time" v-model.trim="route.last_bus_time" />
      </div>
      <div class="p-field">
        <label for="peak_interval">高峰间隔 (分钟)</label>
        <InputNumber id="peak_interval" v-model="route.peak_interval" />
      </div>
      <div class="p-field">
        <label for="off_peak_interval">平时间隔 (分钟)</label>
        <InputNumber id="off_peak_interval" v-model="route.off_peak_interval" />
      </div>
      <div class="p-field">
        <label for="mileage">里程</label>
        <InputNumber
          id="mileage"
          v-model="route.mileage"
          mode="decimal"
          :minFractionDigits="1"
        />
      </div>
      <div class="p-field">
        <label for="start_station">始发站</label>
        <InputText id="start_station" v-model.trim="route.start_station" />
      </div>
      <div class="p-field">
        <label for="end_station">终点站</label>
        <InputText id="end_station" v-model.trim="route.end_station" />
      </div>

      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="hideRouteDialog"
        />
        <Button
          label="保存"
          icon="pi pi-check"
          class="p-button-text"
          @click="saveRoute"
        />
      </template>
    </Dialog>

    <!-- 删除确认框 -->
    <Dialog
      v-model:visible="deleteRouteDialog"
      :style="{ width: '450px' }"
      header="确认删除"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
        <span v-if="route"
          >确定要删除线路
          <b>{{ route.route_name }}</b> 吗？此操作不可撤销。</span
        >
      </div>
      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="deleteRouteDialog = false"
        />
        <Button
          label="确认删除"
          icon="pi pi-check"
          class="p-button-text p-button-danger"
          @click="deleteRoute"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Textarea from "primevue/textarea";
import { useToast } from "primevue/usetoast";
import apiManager from "@/services/api";

const toast = useToast();
const routes = ref([]);
const loading = ref(false);
const routeDialog = ref(false);
const deleteRouteDialog = ref(false);
const route = ref({});
const submitted = ref(false);
const editMode = ref(false);

// 设置过滤器初始状态
const filters = ref({
  global: { value: null, matchMode: "contains" },
});

// 加载线路数据
const loadRoutes = async () => {
  loading.value = true;
  try {
    const response = await apiManager.getAllRoutes();
    routes.value = responseAdapter(response);
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "加载失败",
      detail: "无法获取线路数据",
      life: 3000,
    });
    console.error("获取线路数据失败:", error);
  } finally {
    loading.value = false;
  }
};

// 添加响应适配器函数
const responseAdapter = (response) => {
  if (!Array.isArray(response) || !response.every(Array.isArray)) {
    console.warn("API 响应格式不符合预期，期望二维数组。", response);
    return [];
  }
  return response
    .map((route) => {
      return {
        route_id: route[0],
        route_name: route[1],
        mileage: route[2] || 0,
        first_bus_time: route[3],
        last_bus_time: route[4],
        peak_interval: route[5],
        off_peak_interval: route[6],
        start_station: route[7] || "",
        end_station: route[8] || "",
      };
    })
    .filter(Boolean);
};

// 打开新增线路对话框
const openNewRouteDialog = () => {
  route.value = {
    route_id: "",
    route_name: "",
    mileage: 0,
    first_bus_time: "",
    last_bus_time: "",
    peak_interval: 0,
    off_peak_interval: 0,
    start_station: "",
    end_station: "",
  };
  submitted.value = false;
  routeDialog.value = true;
  editMode.value = false;
};

// 打开编辑线路对话框
const editRoute = (data) => {
  route.value = { ...data };
  routeDialog.value = true;
  editMode.value = true;
};

// 隐藏对话框
const hideRouteDialog = () => {
  routeDialog.value = false;
  submitted.value = false;
};

// 保存线路数据
const saveRoute = async () => {
  submitted.value = true;

  if (!route.value.route_id || !route.value.route_name) {
    return;
  }

  try {
    loading.value = true;
    if (editMode.value) {
      // 更新现有线路
      await apiManager.updateRoute(route.value.route_id, {
        route_name: route.value.route_name,
        mileage: route.value.mileage,
        first_bus_time: route.value.first_bus_time,
        last_bus_time: route.value.last_bus_time,
        peak_interval: route.value.peak_interval,
        off_peak_interval: route.value.off_peak_interval,
        start_station: route.value.start_station,
        end_station: route.value.end_station,
      });
      toast.add({
        severity: "success",
        summary: "操作成功",
        detail: "线路已更新",
        life: 3000,
      });
    } else {
      // 添加新线路
      await apiManager.addRoute({
        route_id: route.value.route_id,
        route_name: route.value.route_name,
        mileage: route.value.mileage,
        first_bus_time: route.value.first_bus_time,
        last_bus_time: route.value.last_bus_time,
        peak_interval: route.value.peak_interval,
        off_peak_interval: route.value.off_peak_interval,
        start_station: route.value.start_station,
        end_station: route.value.end_station,
      });
      toast.add({
        severity: "success",
        summary: "操作成功",
        detail: "线路已添加",
        life: 3000,
      });
    }
    routeDialog.value = false;
    await loadRoutes();
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: editMode.value ? "更新线路失败" : "添加线路失败",
      life: 3000,
    });
    console.error("保存线路失败:", error);
  } finally {
    loading.value = false;
  }
};

// 确认删除线路
const confirmDeleteRoute = (data) => {
  route.value = data;
  deleteRouteDialog.value = true;
};

// 删除线路
const deleteRoute = async () => {
  try {
    loading.value = true;
    await apiManager.deleteRoute(route.value.route_id);
    deleteRouteDialog.value = false;
    await loadRoutes();
    toast.add({
      severity: "success",
      summary: "操作成功",
      detail: "线路已删除",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: "删除线路失败",
      life: 3000,
    });
    console.error("删除线路失败:", error);
  } finally {
    loading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadRoutes();
});
</script>

<style lang="scss" scoped>
.bus-route-modify {
  .route-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    h2 {
      margin: 0;
    }
  }

  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
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
