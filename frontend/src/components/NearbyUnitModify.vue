<template>
  <div class="nearby-unit-modify">
    <div class="unit-header">
      <h2>沿线单位管理</h2>
      <Button label="添加单位" icon="pi pi-plus" @click="openNewUnitDialog" />
    </div>

    <DataTable
      :value="units"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[5, 10, 20, 50]"
      responsiveLayout="scroll"
      class="p-datatable-sm"
      :loading="loading"
      v-model:filters="filters"
      filterDisplay="menu"
      :globalFilterFields="['name', 'address', 'category']"
    >
      <template #header>
        <div class="table-header">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              placeholder="搜索单位..."
            />
          </span>
        </div>
      </template>
      <Column field="unit_id" header="单位编号" sortable></Column>
      <Column field="name" header="单位名称" sortable></Column>
      <Column field="contact_phone" header="联系电话"></Column>
      <Column header="经度/纬度">
        <template #body="slotProps">
          {{ slotProps.data.latitude }}/{{ slotProps.data.longitude }}
        </template>
      </Column>
      <Column field="distance_to_stop" header="距离站点(km)"></Column>
      <Column field="nearby_stop_name" header="附近站点"></Column>
      <Column header="操作">
        <template #body="slotProps">
          <Button
            label="改"
            icon="pi pi-pencil"
            class="p-button-rounded p-button-success p-button-sm p-mr-2"
            @click="editUnit(slotProps.data)"
          />
          <Button
            label="删"
            icon="pi pi-trash"
            class="p-button-rounded p-button-danger p-button-sm"
            @click="confirmDeleteUnit(slotProps.data)"
          />
        </template>
      </Column>
    </DataTable>

    <!-- 添加/编辑单位对话框 -->
    <Dialog
      v-model:visible="unitDialog"
      :style="{ width: '500px' }"
      :header="editMode ? '编辑单位' : '添加单位'"
      :modal="true"
      class="p-fluid"
    >
      <div class="p-field">
        <label for="unit_id">单位编号</label>
        <InputText
          id="unit_id"
          v-model.trim="unit.unit_id"
          required="true"
          autofocus
          :class="{ 'p-invalid': submitted && !unit.unit_id }"
          :disabled="editMode"
        />
        <small class="p-error" v-if="submitted && !unit.unit_id"
          >单位编号必填</small
        >
      </div>
      <div class="p-field">
        <label for="name">单位名称</label>
        <InputText
          id="name"
          v-model.trim="unit.name"
          required="true"
          autofocus
          :class="{ 'p-invalid': submitted && !unit.name }"
        />
        <small class="p-error" v-if="submitted && !unit.name"
          >单位名称必填</small
        >
      </div>
      <div class="p-field">
        <label for="contact_phone">联系电话</label>
        <InputText id="contact_phone" v-model.trim="unit.contact_phone" />
      </div>
      <div class="p-field">
        <label for="latitude">经度</label>
        <InputText id="latitude" v-model.trim="unit.latitude" type="number" />
      </div>
      <div class="p-field">
        <label for="longitude">纬度</label>
        <InputText id="longitude" v-model.trim="unit.longitude" type="number" />
      </div>
      <div class="p-field">
        <label for="distance-to-stop">距离站点(km)</label>
        <InputText
          id="distance-to-stop"
          v-model.trim="unit.distance_to_stop"
          type="number"
        />
      </div>
      <div class="p-field">
        <label for="nearby_stop_id">附近站点</label>
        <Dropdown
          id="nearby_stop_id"
          v-model="unit.nearby_stop_id"
          :options="stops"
          optionLabel="name"
          optionValue="_id"
          placeholder="选择附近站点"
          :filter="true"
        />
      </div>
      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="hideUnitDialog"
        />
        <Button
          label="保存"
          icon="pi pi-check"
          class="p-button-text"
          @click="saveUnit"
        />
      </template>
    </Dialog>

    <!-- 删除确认框 -->
    <Dialog
      v-model:visible="deleteUnitDialog"
      :style="{ width: '450px' }"
      header="确认删除"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
        <span v-if="unit"
          >确定要删除单位 <b>{{ unit.name }}</b> 吗？此操作不可撤销。</span
        >
      </div>
      <template #footer>
        <Button
          label="取消"
          icon="pi pi-times"
          class="p-button-text"
          @click="deleteUnitDialog = false"
        />
        <Button
          label="确认删除"
          icon="pi pi-check"
          class="p-button-text p-button-danger"
          @click="deleteUnit"
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
import Dropdown from "primevue/dropdown";
import Textarea from "primevue/textarea";
import { useToast } from "primevue/usetoast";
import apiManager from "@/services/api";

const toast = useToast();
const units = ref([]);
const stops = ref([]);
const loading = ref(false);
const unitDialog = ref(false);
const deleteUnitDialog = ref(false);
const unit = ref({});
const submitted = ref(false);
const editMode = ref(false);

// 设置过滤器初始状态
const filters = ref({
  global: { value: null, matchMode: "contains" },
});

// 加载单位数据
const loadUnits = async () => {
  loading.value = true;
  try {
    const response = await apiManager.getNearbyUnits();
    if (response) {
      units.value = responseAdapter(response);

      // 如果已加载站点数据，更新单位中的站点名称
      if (stops.value.length > 0) {
        units.value = units.value.map((unit) => {
          const matchingStop = stops.value.find(
            (stop) => stop._id === unit.nearby_stop_id
          );
          if (matchingStop) {
            return { ...unit, nearby_stop_name: matchingStop.name };
          }
          return unit;
        });
      }
    } else {
      console.warn("无法解析单位数据响应", response);
      units.value = [];
    }
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "加载失败",
      detail: "无法获取单位数据",
      life: 3000,
    });
    console.error("获取单位数据失败:", error);
    units.value = [];
  } finally {
    loading.value = false;
  }
};

// 添加响应适配器函数
const responseAdapter = (response) => {
  if (!response || !Array.isArray(response)) {
    console.warn("API 响应格式不符合预期", response);
    return [];
  }
  return response.map((unit) => {
    return {
      unit_id: unit[0],
      name: unit[1],
      contact_phone: unit[2],
      latitude: unit[3],
      longitude: unit[4],
      nearby_stop_id: unit[5],
      nearby_stop_name: "", // 将根据站点列表更新
      distance_to_stop: unit[6],
    };
  });
};

// 加载站点数据（用于选择附近站点）
const loadStops = async () => {
  try {
    const response = await apiManager.getAllStops();
    if (response) {
      const stopsData = response.map((stop) => {
        return {
          _id: stop[0],
          name: stop[1],
          latitude: stop[2],
          longitude: stop[3],
        };
      });

      stops.value = stopsData;

      // 更新单位中的站点名称
      if (units.value.length > 0 && stopsData.length > 0) {
        units.value = units.value.map((unit) => {
          const matchingStop = stopsData.find(
            (stop) => stop._id === unit.nearby_stop_id
          );
          if (matchingStop) {
            return { ...unit, nearby_stop_name: matchingStop.name };
          }
          return unit;
        });
      }
    } else {
      console.warn("无法解析站点数据响应", response);
      stops.value = [];
    }
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "加载失败",
      detail: "无法获取站点数据",
      life: 3000,
    });
    console.error("获取站点数据失败:", error);
    stops.value = [];
  }
};

// 打开新增单位对话框
const openNewUnitDialog = () => {
  unit.value = {
    name: "",
    category: null,
    address: "",
    nearby_stop_id: null,
    contact_phone: "",
    description: "",
  };
  submitted.value = false;
  unitDialog.value = true;
  editMode.value = false;
};

// 打开编辑单位对话框
const editUnit = (data) => {
  unit.value = { ...data };
  unitDialog.value = true;
  editMode.value = true;
};

// 隐藏对话框
const hideUnitDialog = () => {
  unitDialog.value = false;
  submitted.value = false;
};

// 保存单位数据
const saveUnit = async () => {
  submitted.value = true;

  if (!unit.value.name) {
    return;
  }

  try {
    loading.value = true;

    // 根据后端API结构转换数据
    const unitData = {
      unit_id: unit.value.unit_id || "",
      unit_name: unit.value.name,
      contact_phone: unit.value.contact_phone,
      latitude: unit.value.latitude,
      longitude: unit.value.longitude,
      nearby_stop_id: unit.value.nearby_stop_id,
      distance_to_stop: unit.value.distance_to_stop || 0,
    };

    if (editMode.value) {
      // 更新现有单位 - 根据API只发送需要更新的字段
      const updateData = {};
      if (unit.value.name) updateData.unit_name = unit.value.name;
      if (unit.value.contact_phone !== undefined)
        updateData.contact_phone = unit.value.contact_phone;
      if (unit.value.latitude !== undefined)
        updateData.latitude = unit.value.latitude;
      if (unit.value.longitude !== undefined)
        updateData.longitude = unit.value.longitude;
      if (unit.value.nearby_stop_id !== undefined)
        updateData.nearby_stop_id = unit.value.nearby_stop_id;
      if (unit.value.distance_to_stop !== undefined)
        updateData.distance_to_stop = unit.value.distance_to_stop;

      await apiManager.updateNearbyUnit(unit.value.unit_id, updateData);
      toast.add({
        severity: "success",
        summary: "操作成功",
        detail: "单位已更新",
        life: 3000,
      });
    } else {
      // 添加新单位
      await apiManager.addNearbyUnit(unitData);
      toast.add({
        severity: "success",
        summary: "操作成功",
        detail: "单位已添加",
        life: 3000,
      });
    }
    unitDialog.value = false;
    await loadUnits();
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: editMode.value ? "更新单位失败" : "添加单位失败",
      life: 3000,
    });
    console.error("保存单位失败:", error);
  } finally {
    loading.value = false;
  }
};

// 确认删除单位
const confirmDeleteUnit = (data) => {
  unit.value = data;
  deleteUnitDialog.value = true;
};

// 删除单位
const deleteUnit = async () => {
  try {
    loading.value = true;
    // 确保使用正确的ID字段
    await apiManager.deleteNearbyUnit(unit.value.unit_id);
    deleteUnitDialog.value = false;
    await loadUnits();
    toast.add({
      severity: "success",
      summary: "操作成功",
      detail: "单位已删除",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "操作失败",
      detail: "删除单位失败",
      life: 3000,
    });
    console.error("删除单位失败:", error);
  } finally {
    loading.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadUnits();
  loadStops();
});
</script>

<style lang="scss" scoped>
.nearby-unit-modify {
  .unit-header {
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
