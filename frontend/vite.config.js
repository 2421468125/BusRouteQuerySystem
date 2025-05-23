import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import fs from 'fs'

const jsonData = JSON.parse(fs.readFileSync('backend/app/settings.json', 'utf-8'));

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/assets/main.scss" as *;`,
      },
    },
  },
  define:{
    __BASE_URL__: JSON.stringify(jsonData.ServerHost+':'+jsonData.ServerPort),
  },
})
