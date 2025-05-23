<template>
  <div class="home-container">
    <Menubar :model="items" class="app-menubar">
      <template #start>
        <img alt="logo" src="../assets/logo.png" height="40" class="p-mr-2" />
        <span class="app-title">公交信息管理系统</span>
      </template>
      <template #end>
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
// 导入子组件
import BusRoutes from "@/components/BusRoutes.vue";
import BusStops from "@/components/BusStops.vue";
import NearbyUnits from "@/components/NearbyUnits.vue";

const router = useRouter();

// 导航菜单项
const items = ref([
  { label: "公交线路", icon: "pi pi-compass", component: "BusRoutes" },
  { label: "公交站点", icon: "pi pi-map-marker", component: "BusStops" },
  { label: "沿线单位", icon: "pi pi-building", component: "NearbyUnits" },
]);

// 当前选中的选项卡，默认显示第一个
const activeItem = ref(items.value[0]);

// 监听 TabMenu 的 tabChange 事件来更新 activeItem
// TabMenu 组件没有直接的 v-model，但你可以通过 @tab-change 事件来控制
// 这里我们使用计算属性来动态绑定 component
const currentTabComponent = computed(() => {
  switch (activeItem.value.component) {
    case "BusRoutes":
      return BusRoutes;
    case "BusStops":
      return BusStops;
    case "NearbyUnits":
      return NearbyUnits;
    default:
      return null;
  }
});

// PrimeVue TabMenu 没有直接的 v-model，需要手动处理点击事件来切换 activeItem
const handleTabClick = (event) => {
  activeItem.value = event.item;
};

// 重写 TabMenu 的 items 结构以包含 command 属性来更新 activeItem
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
</script>

<style lang="scss" scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa; // 轻微的背景色
}

.app-menubar {
  background-color: #424242; // 深色背景
  color: #ffffff; // 白色文字
  padding: 0.8rem 1.5rem;
  border-radius: 0; // 移除圆角
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
    color: #ffcccc !important; // 退出按钮颜色
    &:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
}

.tab-navigation {
  margin-top: 0; // 紧贴顶部导航栏
  background-color: #ffffff;
  border-bottom: 1px solid #dee2e6;
  .p-tabmenu-nav {
    justify-content: center; // 选项卡居中
  }
  .p-menuitem-link {
    padding: 1rem 1.5rem; // 增加点击区域
  }
}

.content-panel {
  flex-grow: 1; // 填充剩余空间
  padding: 2rem;
  background-color: #ffffff;
  margin: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

// 确保 logo.png 在 src/assets 目录下
</style>
