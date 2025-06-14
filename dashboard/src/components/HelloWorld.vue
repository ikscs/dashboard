<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref('Загрузка...')
const error = ref(null)
const loading = ref(false)

const fetchMessage = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await axios.get('http://localhost:8000/api/hello/')
    message.value = response.data.message
  } catch (err) {
    error.value = 'Ошибка при загрузке данных: ' + err.message
    message.value = 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchMessage()
})
</script>

<template>
  <div class="hello-world">
    <h1>{{ message }}</h1>
    <p v-if="error" class="error">{{ error }}</p>
    <v-btn
      color="primary"
      @click="fetchMessage"
      :loading="loading"
      class="mt-4"
    >
      Обновить
    </v-btn>
  </div>
</template>

<style scoped>
.hello-world {
  text-align: center;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  margin: 2rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.error {
  color: #ff4444;
  margin: 1rem 0;
  padding: 1rem;
  background-color: #ffebee;
  border-radius: 4px;
}

.mt-4 {
  margin-top: 1rem;
}
</style>
