import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const id = ref("")
  const first_name = ref("")
  const last_name = ref("")
  const email = ref("")
  const username = ref("")
  return { id, first_name, last_name, email, username }
})