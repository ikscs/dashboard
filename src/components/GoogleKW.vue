<template>
  <div class="google-kw-page">
    <v-card class="mt-6">
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-google</v-icon>
        Google Search Console Keywords
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
          <v-btn
            color="primary"
            class="mt-4"
            @click="fetchData"
            prepend-icon="mdi-refresh"
          >
            Повторить
          </v-btn>
        </div>
        
        <div v-else-if="data && data.length > 0" class="table-container">
          <v-table>
            <thead>
              <tr>
                <th v-for="header in headers" :key="header.key" class="text-left">
                  {{ header.title }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(item, index) in data" 
                :key="index"
                :class="getRowClass(item)"
              >
                <td v-for="header in headers" :key="header.key">
                  <span v-if="item[header.key] === null || item[header.key] === undefined" class="text-grey">
                    -
                  </span>
                  <span v-else-if="typeof item[header.key] === 'object'">
                    {{ JSON.stringify(item[header.key]) }}
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
            Данные не найдены
          </v-alert>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS, API_HEADERS } from '../config/api'

const loading = ref(false)
const error = ref(null)
const data = ref([])

// Автоматически генерируем заголовки на основе первого элемента данных
const headers = computed(() => {
  if (!data.value || data.value.length === 0) return []
  
  const firstItem = data.value[0]
  // Поля, которые нужно скрыть
  const excludedFields = ['pos_prev', 'posPrev', 'Pos Prev', 'show_prev', 'showPrev', 'Show Prev']
  
  return Object.keys(firstItem)
    .filter(key => !excludedFields.includes(key.toLowerCase()) && !excludedFields.includes(key))
    .map(key => ({
      key: key,
      title: key.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ')
    }))
})

// Функция для определения класса строки на основе Pos Delta
const getRowClass = (item) => {
  // Проверяем разные возможные названия поля
  const posDelta = item.pos_delta ?? item.posDelta ?? item['pos_delta'] ?? item['Pos Delta'] ?? null
  
  if (posDelta === null || posDelta === undefined) {
    return ''
  }
  
  // Преобразуем в число, если это строка
  const deltaValue = typeof posDelta === 'string' 
    ? parseFloat(posDelta.replace(/[^\d.-]/g, '')) 
    : Number(posDelta)
  
  if (isNaN(deltaValue)) {
    return ''
  }
  
  if (deltaValue > 0) {
    return 'row-positive'
  } else if (deltaValue < 0) {
    return 'row-negative'
  }
  
  return ''
}

const fetchData = async () => {
  loading.value = true
  error.value = null
  
  try {
    console.log('Запрос к V_GOOGLE_KW:', API_ENDPOINTS.V_GOOGLE_KW)
    console.log('Заголовки SEO:', API_HEADERS.SEO)
    
    const response = await axios.get(API_ENDPOINTS.V_GOOGLE_KW, {
      headers: API_HEADERS.SEO
    })
    
    console.log('Ответ API:', response.data)
    const responseData = Array.isArray(response.data) ? response.data : []
    data.value = responseData
    
    console.log('Загружено данных:', responseData.length)
  } catch (err) {
    console.error('Ошибка загрузки данных:', err)
    error.value = err.response?.data?.message || err.message || 'Ошибка при загрузке данных'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.google-kw-page {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

:deep(.v-card) {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin: 0;
}

:deep(.v-card-text) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 16px !important;
}

.table-container {
  flex: 1;
  overflow: auto;
  position: relative;
  margin-right: -16px;
  margin-bottom: -16px;
  padding-right: 16px;
  padding-bottom: 16px;
}

:deep(.v-table) {
  width: 100%;
}

:deep(.v-table th) {
  background-color: #e3f2fd;
  font-weight: 700;
  color: #1565c0;
  padding: 12px;
  border-bottom: 3px solid #1976d2;
  position: sticky;
  top: 0;
  z-index: 1;
}

:deep(.v-table td) {
  padding: 8px 12px;
  border-bottom: 1px solid #f0f0f0;
}

/* Зелёный цвет для положительных значений Pos Delta */
:deep(.v-table tbody tr.row-positive) {
  background-color: #e8f5e9 !important;
}

:deep(.v-table tbody tr.row-positive:hover) {
  background-color: #c8e6c9 !important;
}

:deep(.v-table tbody tr.row-positive td) {
  border-bottom-color: #a5d6a7;
}

/* Малиновый цвет для отрицательных значений Pos Delta */
:deep(.v-table tbody tr.row-negative) {
  background-color: #fce4ec !important;
}

:deep(.v-table tbody tr.row-negative:hover) {
  background-color: #f8bbd0 !important;
}

:deep(.v-table tbody tr.row-negative td) {
  border-bottom-color: #f48fb1;
}

:deep(.v-table tbody tr:hover) {
  background-color: #f8f9fa;
}

:deep(.v-table tbody tr:nth-child(even)) {
  background-color: #fafafa;
}

/* Переопределяем для окрашенных строк */
:deep(.v-table tbody tr.row-positive:nth-child(even)) {
  background-color: #e8f5e9 !important;
}

:deep(.v-table tbody tr.row-negative:nth-child(even)) {
  background-color: #fce4ec !important;
}
</style>
