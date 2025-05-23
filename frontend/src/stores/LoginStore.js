import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useLoginStore = defineStore('login', () => {
  const isLoggedIn = ref(false)
  const user = ref(null)

  function login(userData) {
    isLoggedIn.value = true
    user.value = userData
  }

  function logout() {
    isLoggedIn.value = false
    user.value = null
  }

  return { isLoggedIn, user, login, logout }
})