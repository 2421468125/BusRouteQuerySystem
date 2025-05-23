<template>
  <div class="bus-stops-modify">
    <div class="stops-header">
      <h2>公交站点管理</h2>
      <Button label="添加站点" icon="pi pi-plus" @click="openNewStopDialog" />
    </div>

    <DataTable
      :value="stops"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      responsiveLayout="scroll"
      class="p-datatable-sm"
      :loading="loading"
      v-model:filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['stop_name', 'stop_id']"
    >
      <template #header>
        <div class="table-header">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              placeholder="搜索站点..."
            />
          </span>
        </div>
      </template>

      <Column field="stop_id" header="站点编号" sortable></Column>
      <Column field="stop_name" header="站点名称" sortable></Column>
      <Column field="latitude" header="纬度"></Column>
      <Column field="longitude" header="经度"></Column>
      <Column header="操作">
        <template #body="slotProps">
          <Button
            label="改"
            icon="pi pi-pencil"
            class="p-button-rounded p-button-success p-button-sm p-mr-2"
            @click="editStop(slotProps.data)"
          />
          <Button
            label="删"
            icon="pi pi-trash"
            class="p-button-rounded p-button-danger p-button-sm"
            @click="confirmDeleteStop(slotProps.data)"
          />
        </template>
      </Column>
    </DataTable>

    <!-- 添加/编辑站点对话框 -->
    <Dialog
      v-model:visible="stopDialog"
      :style="{ width: '500px' }"
      :header="editMode ? '编辑站点' : '添加站点'"
      :modal="true"
      class="p-fluid"
    >
      <div class="p-field">
        <label for="stop_id">站点编号</label>
        <InputText
          id="stop_id"
          v-model.trim="stop.stop_id"
          required="true"
          autofocus
          :class="{ 'p-invalid': submitted && !stop.stop_id }"
          :disabled="editMode"
        />
        <small class="p-error" v-if="submitted && !stop.stop_id"
          >站点编号必填</small
        >
      </div>
      <div class="p-field">
        <label for="stop_name">站点名称</label>
        <InputText
          id="stop_name"
          v-model.trim="stop.stop_name"
          required="true"
          :class="{ 'p-invalid': submitted && !stop.stop_name }"
        />
        <small class="p-error" v-if="submitted && !stop.stop_name"
          >站点名称必填</small
        >
      </div>
      <div class="p-field">
        <label for="latitude">纬度</label>
        <InputNumber
          id="latitude"
          v-model="stop.latitude"
          mode="decimal"
          :minFractionDigits="6"
          :maxFractionDigits="6"
        />
      </div>
      <div class="p-field">
        <label for="longitude">经度</label>
        <InputNumber
          id="longitude"
          v-model="stop.longitude"
          mode="decimal"
          :minFractionDigits="6"
          :maxFractionDigits="6"
        />
      </div>

      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="hideStopDialog"
        />
        <Button
          label="保存"
          icon="pi pi-check"
          class="p-button-text"
          @click="saveStop"
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
        <span v-if="stop"
          >确定要删除站点 <b>{{ stop.stop_name }}</b> 吗？此操作不可撤销。</span
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
          @click="deleteStop"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
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
const stops = ref([]);
const loading = ref(false);
const stopDialog = ref(false);
const deleteStopDialog = ref(false);
const stop = ref({});
const submitted = ref(false);
const editMode = ref(false);

// 设置过滤器初始状态
const filters = ref({
  global: { value: null, matchMode: "contains" },
});

// 加载站点数据
const loadStops = async () => {
  loading.value = true;
  try {
    const response = await apiManager.getAllStops();
    stops.value = responseAdapter(response);
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "加载失败",
      detail: "无法获取站点数据",
      life: 3000,
    });
    console.error("获取站点数据失败:", error);
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
    .map((stop) => {
      return {
        stop_id: stop[0],
        stop_name: stop[1],
        latitude: stop[2],
        longitude: stop[3],
      };
    })
    .filter(Boolean);
};

// 打开新增站点对话框
const openNewStopDialog = () => {
  stop.value = {
    stop_id: "",
    stop_name: "",
    latitude: null,
    longitude: null,
  };
  submitted.value = false;
  stopDialog.value = true;
  editMode.value = false;
};

// 打开编辑站点对话框
const editStop = (data) => {
  stop.value = { ...data };
  stopDialog.value = true;
  editMode.value = true;
};

// 隐藏对话框
const hideStopDialog = () => {
  stopDialog.value = false;
  submitted.value = false;
};

// 保存站点数据
const saveStop = async () => {
  submitted.value = true;

  if (!stop.value.stop_id || !stop.value.stop_name) {
    return;
  }

  try {
    loading.value = true;
    if (editMode.value) {
      // 更新现有站点
      await apiManager.updateStop(stop.value.stop_id, {
        stop_name: stop.value.stop_name,
        latitude: stop.value.latitude,
        longitude: stop.value.longitude,
      });
      toast.add({
        severity: "success",
        summary: "操作成功",
        detail: "站点已更新",
        life: 3000,
      });
    } else {
      // 添加新站点
      await apiManager.addStop({
        stop_id: stop.value.stop_id,
        stop_name: stop.value.stop_name,
        latitude: stop.value.latitude,
        longitude: stop.value.longitude,
      });
      toast.add({
        severity: "success",
        summary: "操作成功",
        detail: "站点已添加",
        life: 3000,
      });
    }
    stopDialog.value = false;
    await loadStops();
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: editMode.value ? "更新站点失败" : "添加站点失败",
      life: 3000,
    });
    console.error("保存站点失败:", error);
  } finally {
    loading.value = false;
  }
};

// 确认删除站点
const confirmDeleteStop = (data) => {
  stop.value = data;
  deleteStopDialog.value = true;
};

// 删除站点
const deleteStop = async () => {
  try {
    loading.value = true;
    await apiManager.deleteStop(stop.value.stop_id);
    deleteStopDialog.value = false;
    await loadStops();
    toast.add({
      severity: "success",
      summary: "操作成功",
      detail: "站点已删除",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: "删除站点失败",
      life: 3000,
    });
    console.error("删除站点失败:", error);
  } finally {
    loading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadStops();
});
</script>

<style lang="scss" scoped>
.bus-stops-modify {
  .stops-header {
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
