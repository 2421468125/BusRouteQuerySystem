<template>
  <div class="modify-container">
    <Menubar :model="items" class="app-menubar">
      <template #start>
        <img alt="logo" src="../assets/logo.png" height="40" class="p-mr-2" />
        <span class="app-title">公交线路管理系统——修改</span>
      </template>
      <template #end>
        <Button
          label="返回首页"
          icon="pi pi-home"
          class="p-button-primary p-button-rounded p-mr-2"
          @click="goToHome"
        />
        <Button
          label="退出登录"
          icon="pi pi-sign-out"
          class="p-button-danger p-button-text"
          @click="logout"
        />
      </template>
    </Menubar>

    <TabMenu :model="items" class="tab-navigation" />

    <div class="content-panel">
      <component :is="currentTabComponent" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import TabMenu from "primevue/tabmenu";
import Menubar from "primevue/menubar";
import Button from "primevue/button";
import { useLoginStore } from "@/stores/loginStore";
// 导入修改组件
import BusRouteModify from "@/components/BusRouteModify.vue";
import BusStopsModify from "@/components/BusStopsModify.vue";
import NearbyUnitModify from "@/components/NearbyUnitModify.vue";
import RouteStationModify from "@/components/RouteStationModify.vue";

const router = useRouter();

// 导航菜单项
const items = ref([
  { label: "公交线路管理", icon: "pi pi-compass", component: "BusRouteModify" },
  {
    label: "公交站点管理",
    icon: "pi pi-map-marker",
    component: "BusStopsModify",
  },
  {
    label: "沿线单位管理",
    icon: "pi pi-building",
    component: "NearbyUnitModify",
  },
  {
    label: "线路站点关系管理",
    icon: "pi pi-sitemap",
    component: "RouteStationModify",
  },
]);

// 当前选中的选项卡，默认显示第一个
const activeItem = ref(items.value[0]);

// 计算当前应该显示的组件
const currentTabComponent = computed(() => {
  switch (activeItem.value.component) {
    case "BusRouteModify":
      return BusRouteModify;
    case "BusStopsModify":
      return BusStopsModify;
    case "NearbyUnitModify":
      return NearbyUnitModify;
    case "RouteStationModify":
      return RouteStationModify;
    default:
      return null;
  }
});

// 为每个菜单项添加命令函数
items.value.forEach((item) => {
  item.command = () => {
    activeItem.value = item;
  };
});

const logout = () => {
  localStorage.removeItem("loggedInUser");
  useLoginStore().logout();
  router.push("/login");
};

// 返回首页
const goToHome = () => {
  router.push("/home");
};
</script>

<style lang="scss" scoped>
.modify-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.app-menubar {
  background-color: #424242;
  color: #ffffff;
  padding: 0.8rem 1.5rem;
  border-radius: 0;
  .p-menubar-start {
    display: flex;
    align-items: center;
  }
  .app-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-left: 0.5rem;
    color: #ffffff;
  }
  .p-button-danger.p-button-text {
    color: #ffcccc !important;
    &:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
}

.tab-navigation {
  margin-top: 0;
  background-color: #ffffff;
  border-bottom: 1px solid #dee2e6;
  .p-tabmenu-nav {
    justify-content: center;
  }
  .p-menuitem-link {
    padding: 1rem 1.5rem;
  }
}

.content-panel {
  flex-grow: 1;
  padding: 2rem;
  background-color: #ffffff;
  margin: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
</style>
