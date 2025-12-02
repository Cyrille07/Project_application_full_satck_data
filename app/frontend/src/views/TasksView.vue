<template>
  <div>
    <h2>📋 Liste des tâches</h2>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        {{ task.title }} — {{ task.status }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const tasks = ref([])
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001"

const fetchTasks = async () => {
  const res = await axios.get(`${API_URL}/tasks`)
  tasks.value = res.data
}

onMounted(fetchTasks)
</script>
