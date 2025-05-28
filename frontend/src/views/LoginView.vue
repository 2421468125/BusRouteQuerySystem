<template>
  <div class="login-container">
    <p class="title">公交线路管理系统</p>
    <Card class="p-card login-card">
      <template #title> 登录 </template>
      <template #content>
        <div class="p-fluid">
          <div class="p-field">
            <label for="username">用户名</label>
            <InputText id="username" v-model="username" type="text" />
          </div>
          <div class="p-field">
            <label for="password">密码</label>
            <Password
              id="password"
              v-model="password"
              :feedback="false"
              toggleMask
            />
          </div>
          <Button
            label="登录"
            icon="pi pi-sign-in"
            @click="handleLogin"
            class="p-mt-3"
          />
          <Message v-if="errorMessage" severity="error" :closable="false">{{
            errorMessage
          }}</Message>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";
import Message from "primevue/message";
import { useLoginStore } from "@/stores/loginStore";

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const router = useRouter(); // 获取路由实例
const loginStore = useLoginStore();
const { login, logout } = loginStore;

// 默认用户和密码
const DEFAULT_USERNAME = "admin";
const DEFAULT_PASSWORD = "123456";
const CACHE_KEY = "loggedInUser"; // localStorage 缓存键
const CACHE_EXPIRATION_HOURS = 1; // 缓存有效期，单位小时

// 处理登录逻辑
const handleLogin = () => {
  errorMessage.value = "";

  if (
    username.value === DEFAULT_USERNAME &&
    password.value === DEFAULT_PASSWORD
  ) {
    const loginInfo = {
      username: username.value,
      loggedIn: true,
      timestamp: Date.now(), // 记录登录时间戳
    };
    localStorage.setItem(CACHE_KEY, JSON.stringify(loginInfo));
    console.log("登录成功！欢迎回来，", username.value);

    // 假设登录成功后跳转到主页或其他页面
    login(username.value);
    router.push("/home");
  } else {
    errorMessage.value = "用户名或密码不正确！";
  }
};

// 检查缓存并尝试自动登录
onMounted(() => {
  const cachedLoginInfo = localStorage.getItem(CACHE_KEY);
  if (cachedLoginInfo) {
    try {
      const loginInfo = JSON.parse(cachedLoginInfo);
      const currentTime = Date.now();
      const loginTime = loginInfo.timestamp;
      const expirationTime = CACHE_EXPIRATION_HOURS * 60 * 60 * 1000; // 1小时的毫秒数

      if (loginInfo.loggedIn && currentTime - loginTime < expirationTime) {
        console.log(
          "检测到有效缓存，自动登录成功！欢迎回来，",
          loginInfo.username
        );
        login(loginInfo.username);
        router.push("/home");
      } else {
        localStorage.removeItem(CACHE_KEY);
      }
    } catch (e) {
      console.error("解析缓存信息失败", e);
      localStorage.removeItem(CACHE_KEY); // 解析失败也清除缓存
    }
  }
});
</script>

<style lang="scss" scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}
.title {
  font-size: 3rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.p-fluid .p-field {
  margin-bottom: 1.5rem;
}

.p-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.p-inputtext,
.p-password {
  width: 100%;
}

.p-button {
  width: 100%;
}

.p-message {
  margin-top: 1rem;
}
</style>
