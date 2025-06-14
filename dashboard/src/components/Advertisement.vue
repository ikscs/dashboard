<template>
  <div class="advertisement-container">
    <h2>Реклама</h2>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="advertisement-data">
      <div v-for="ad in advertisements" :key="ad.id" class="advertisement-item">
        <h3>{{ ad.name }}</h3>
        <p>Дата: {{ formatDate(ad.date) }}</p>
        <p>Бюджет: {{ ad.budget }} ₽</p>
        <p>Платформа: {{ ad.platform }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const advertisements = ref([])
const loading = ref(true)
const error = ref(null)

const fetchAdvertisements = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/advertisements/')
    advertisements.value = response.data
    loading.value = false
  } catch (err) {
    error.value = 'Ошибка при загрузке данных: ' + err.message
    loading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ru-RU')
}

onMounted(() => {
  fetchAdvertisements()
})
</script>

<style scoped>
.advertisement-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
  color: #666;
}

.error {
  color: #ff4444;
  padding: 20px;
  text-align: center;
}

.advertisement-data {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.advertisement-item {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.advertisement-item h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.advertisement-item p {
  margin: 5px 0;
  color: #666;
}
</style> 