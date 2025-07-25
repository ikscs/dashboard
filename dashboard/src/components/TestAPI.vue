<template>
  <div class="stat-table-container">
    <v-card class="stat-card">
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-3">mdi-chart-line</v-icon>
        Статистика за 7 дней (сырые данные)
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="testAPI"
          :loading="loading"
          prepend-icon="mdi-refresh"
        >
          Обновить данные
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <div v-if="loading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <div class="mt-4 text-body-1">Загрузка данных...</div>
        </div>
        
        <div v-else-if="error" class="text-center py-8">
          <v-alert type="error" variant="tonal">
            <v-alert-title>Ошибка загрузки</v-alert-title>
            {{ error }}
          </v-alert>
        </div>
        
        <div v-else-if="data && data.length > 0">
          <v-table>
            <thead>
              <tr>
                <th v-for="header in headers" :key="header.key" class="text-left">
                  {{ header.title }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in data" :key="index">
                <td v-for="header in headers" :key="header.key">
                  <span v-if="item[header.key] === null || item[header.key] === undefined" class="text-grey">
                    null
                  </span>
                  <span v-else>
                    {{ item[header.key] }}
                  </span>
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
        
        <div v-else class="text-center py-8">
          <v-alert type="info" variant="tonal">
            <v-alert-title>Нет данных</v-alert-title>
            Нажмите "Обновить данные" для загрузки статистики
          </v-alert>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const data = ref(null)
const loading = ref(false)
const error = ref(null)

// Динамически создаем заголовки на основе данных
const headers = computed(() => {
  if (!data.value || data.value.length === 0) return []
  
  // Получаем все уникальные ключи из первого объекта
  const firstItem = data.value[0]
  if (!firstItem) return []
  
  return Object.keys(firstItem).map(key => ({
    title: key,
    key: key
  }))
})

const testAPI = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get('http://localhost:8000/api/stat-group-7d/')
    console.log('API Response:', response)
    console.log('Response data:', response.data)
    console.log('Response type:', typeof response.data)
    console.log('Is array:', Array.isArray(response.data))
    console.log('Length:', response.data?.length)
    
    data.value = response.data
  } catch (err) {
    console.error('API Error:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// Автоматическая загрузка данных при монтировании компонента
onMounted(() => {
  testAPI()
})
</script>

<style scoped>
.stat-table-container {
  padding: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.v-theme--dark .stat-card {
  background: rgba(30, 30, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.text-grey {
  color: rgba(var(--v-theme-on-surface), 0.5) !important;
  font-style: italic;
}

/* Стили для таблицы */
:deep(.v-table) {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(var(--v-theme-outline), 0.12);
}

:deep(.v-table thead) {
  background-color: rgb(var(--v-theme-surface-variant));
}

:deep(.v-table th) {
  font-weight: 600;
  color: rgb(var(--v-theme-on-surface-variant));
  padding: 12px 16px;
  border-bottom: 1px solid rgba(var(--v-theme-outline), 0.12);
}

:deep(.v-table td) {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(var(--v-theme-outline), 0.08);
}

:deep(.v-table tbody tr:hover) {
  background-color: rgba(var(--v-theme-primary), 0.04);
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .stat-table-container {
    padding: 10px;
  }
  
  :deep(.v-table td),
  :deep(.v-table th) {
    padding: 8px 12px;
    font-size: 0.875rem;
  }
}
</style> 