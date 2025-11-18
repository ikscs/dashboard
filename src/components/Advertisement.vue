<template>
  <div class="advertisement-page">
    <!-- Первая таблица: UTM данные -->
    <v-card class="welcome-card mb-6">
      <v-card-title class="d-flex align-center">
        <v-icon size="large" class="mr-3">mdi-tag-multiple</v-icon>
        UTM данные
      </v-card-title>
    
    <v-card-text>
      <div v-if="utmLoading" class="text-center py-8">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <div class="mt-4 text-body-1">Загрузка UTM данных...</div>
      </div>
      
      <div v-else-if="utmError" class="text-center py-8">
        <v-alert type="error" variant="tonal">
          <v-alert-title>Ошибка загрузки UTM данных</v-alert-title>
          {{ utmError }}
        </v-alert>
      </div>
      
      <div v-else-if="utmData && utmData.length > 0" class="advertisement-scroll">
        <v-table>
          <thead>
            <tr>
              <th v-for="header in utmHeaders" :key="header.key" class="text-left">
                {{ header.title }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in utmData" :key="index">
              <td v-for="header in utmHeaders" :key="header.key">
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
          <v-alert-title>Нет UTM данных</v-alert-title>
          Нажмите "Обновить UTM данные" для загрузки
        </v-alert>
      </div>
    </v-card-text>
  </v-card>

  <!-- Вторая таблица: Статистика рекламы за 7 дней -->
  <v-card class="welcome-card">
    <v-card-title class="d-flex align-center">
      <v-icon size="large" class="mr-3">mdi-google-ads</v-icon>
      Статистика рекламы за 7 дней (сырые данные)
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
      
      <div v-else-if="data && data.length > 0" class="advertisement-scroll">
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
import { API_ENDPOINTS } from '../config/api'

// Данные для первой таблицы (UTM)
const utmData = ref(null)
const utmLoading = ref(false)
const utmError = ref(null)

// Данные для второй таблицы (статистика рекламы)
const data = ref(null)
const loading = ref(false)
const error = ref(null)

// Заголовки для UTM таблицы
const utmHeaders = computed(() => {
  if (!utmData.value || utmData.value.length === 0) return []
  
  const firstItem = utmData.value[0]
  if (!firstItem) return []
  
  return Object.keys(firstItem).map(key => ({
    title: key,
    key: key
  }))
})

// Заголовки для статистики рекламы
const headers = computed(() => {
  if (!data.value || data.value.length === 0) return []
  
  const firstItem = data.value[0]
  if (!firstItem) return []
  
  return Object.keys(firstItem).map(key => ({
    title: key,
    key: key
  }))
})

// Загрузка UTM данных
const loadUtmData = async () => {
  utmLoading.value = true
  utmError.value = null
  
  try {
    const response = await axios.get(API_ENDPOINTS.V_UTM)
    console.log('UTM API Response:', response)
    console.log('UTM Response data:', response.data)
    
    utmData.value = response.data
  } catch (err) {
    console.error('UTM API Error:', err)
    utmError.value = err.message
  } finally {
    utmLoading.value = false
  }
}

// Загрузка данных статистики рекламы
const testAPI = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(API_ENDPOINTS.ADVERTISEMENT)
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
  loadUtmData()
  testAPI()
})
</script>

<style scoped>
.advertisement-page {
  width: 100%;
  height: 100%;
}

.welcome-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.v-theme--dark .welcome-card {
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.text-grey {
  color: rgba(var(--v-theme-on-surface), 0.5) !important;
  font-style: italic;
}

.advertisement-scroll {
  max-height: 60vh;
  overflow-y: auto;
  margin-top: 8px;
  margin-bottom: 8px;
}

/* Стили для таблицы */
:deep(.v-table) {
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(var(--v-theme-outline), 0.12);
}

:deep(.v-table thead) {
  background-color: #e3f2fd;
}

:deep(.v-table th) {
  background-color: #e3f2fd !important;
  font-weight: 700 !important;
  color: #1565c0 !important;
  padding: 12px 16px !important;
  border-bottom: 3px solid #1976d2 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
  font-size: 0.9rem !important;
}

:deep(.v-theme--dark .v-table thead) {
  background-color: #1e3a5f;
}

:deep(.v-theme--dark .v-table th) {
  background-color: #1e3a5f !important;
  color: #90caf9 !important;
  border-bottom: 3px solid #42a5f5 !important;
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
  .advertisement-page {
    padding: 10px;
  }
  .advertisement-scroll {
    max-height: 40vh;
  }
  :deep(.v-table td),
  :deep(.v-table th) {
    padding: 8px 12px;
    font-size: 0.875rem;
  }
}
</style> 