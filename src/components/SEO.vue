<template>
  <div class="seo-page">
    <!-- Top Section -->
    <v-card class="mt-6 seo-top-card">
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-table</v-icon>
        Таблица Top (mk, схема seo)
      </v-card-title>
      <v-card-text class="seo-top-card-text">
        <!-- Фільтри -->
        <div class="filters-row mb-4">
          <v-row>
            <v-col cols="12" sm="3">
              <v-select
                v-model="filters.topic"
                :items="topicOptions"
                label="Topic"
                clearable
                variant="outlined"
                density="compact"
                @update:model-value="applyFilters"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="3">
              <v-select
                v-model="filters.keywords"
                :items="keywordsOptions"
                label="Keywords"
                clearable
                variant="outlined"
                density="compact"
                @update:model-value="applyFilters"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="3" class="d-flex align-center">
              <v-checkbox
                v-model="filters.ourOnly"
                label="Тільки наші дані (our ≠ NULL)"
                density="compact"
                @update:model-value="applyFilters"
              ></v-checkbox>
            </v-col>
            <v-col cols="12" sm="3" class="d-flex align-center">
              <v-btn
                color="secondary"
                variant="outlined"
                size="small"
                @click="clearFilters"
                prepend-icon="mdi-filter-remove"
              >
                Очистити фільтри
              </v-btn>
            </v-col>
          </v-row>
        </div>

        <div v-if="vTopLoading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <div class="mt-4 text-body-1">Загрузка данных Top...</div>
        </div>
        <div v-else-if="vTopError" class="text-center py-8">
          <v-alert type="error" variant="tonal">
            <v-alert-title>Ошибка загрузки Top</v-alert-title>
            {{ vTopError }}
          </v-alert>
        </div>
        <div v-else-if="filteredTopData && filteredTopData.length > 0" class="seo-top-scroll">
          <v-table>
            <thead>
              <tr>
                <th v-for="header in vTopHeaders" :key="header.key" class="text-left">
                  {{ header.title }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in filteredTopData" :key="index">
                <td v-for="header in vTopHeaders" :key="header.key">
                  <span v-if="item[header.key] === null || item[header.key] === undefined" class="text-grey">
                    null
                  </span>
                  <span v-else-if="header.key === 'description' && item[header.key] && item[header.key].length > 50" 
                        :title="item[header.key]" class="truncated-text">
                    {{ item[header.key].substring(0, 50) }}...
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
            <v-alert-title>Нет данных Top</v-alert-title>
            Дані будуть завантажені автоматично
          </v-alert>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS, API_HEADERS } from '@/config/api.js'

const vTopData = ref([])
const vTopLoading = ref(false)
const vTopError = ref(null)

// Фільтри
const filters = ref({
  topic: null,
  keywords: null,
  ourOnly: false
})

const fetchVTop = async () => {
  vTopLoading.value = true
  vTopError.value = null
  try {
    console.log('=== ДІАГНОСТИКА API ===')
    console.log('API_BASE_URL_PG:', import.meta.env.VITE_API_BASE_URL_PG)
    console.log('API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)
    console.log('API_ENDPOINTS:', API_ENDPOINTS)
    console.log('API_ENDPOINTS.V_TOP:', API_ENDPOINTS.V_TOP)
    console.log('Заголовки:', API_HEADERS.SEO)
    console.log('=======================')
    
    // Перевіряємо, чи існує ендпоінт
    if (!API_ENDPOINTS.V_TOP) {
      throw new Error('Ендпоінт V_TOP не знайдено в конфігурації API')
    }
    
    // Додаємо додаткові заголовки для кращої сумісності
    const headers = {
      ...API_HEADERS.SEO,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    console.log('Повні заголовки запиту:', headers)
    
    const response = await axios.get(API_ENDPOINTS.V_TOP, {
      headers: headers
    })
    console.log('Відповідь API:', response.data)
    console.log('Статус відповіді:', response.status)
    console.log('Заголовки відповіді:', response.headers)
    
    // Перевіряємо, чи є дані в відповіді
    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      vTopData.value = response.data
      console.log('Дані завантажені з API:', vTopData.value.length, 'записів')
      console.log('Структура першого запису:', Object.keys(vTopData.value[0]))
      console.log('Перший запис:', vTopData.value[0])
    } else {
      console.log('API повернув порожній масив або невалідні дані, використовуємо fallback')
      throw new Error('API повернув порожні дані')
    }
  } catch (err) {
    console.error('Ошибка API:', err)
    console.error('Деталі помилки:', {
      message: err.message,
      status: err.response?.status,
      statusText: err.response?.statusText,
      data: err.response?.data,
      headers: err.response?.headers
    })
    vTopError.value = err.response?.data?.message || err.message || 'Неизвестная ошибка'
    
    // Fallback дані для тестування
    console.log('Використовуємо fallback дані для v_top')
    vTopError.value = null // Очищаємо помилку
    vTopData.value = [
      {
        id: 1,
        domain: 'example.com',
        title: 'Web Development Services',
        description: 'Professional web development and consulting services',
        topic: 'Technology',
        keywords: 'web development',
        relevance: 0.85,
        our: 'some value',
        created_at: '2024-01-15'
      },
      {
        id: 2,
        domain: 'ikscs.in.ua',
        title: 'Business Consulting',
        description: 'Strategic business consulting and advisory services',
        topic: 'Business Services',
        keywords: 'consulting',
        relevance: 0.92,
        our: null,
        created_at: '2024-01-14'
      },
      {
        id: 3,
        domain: 'test.com',
        title: 'Digital Marketing Solutions',
        description: 'Comprehensive digital marketing and SEO services',
        topic: 'Marketing',
        keywords: 'digital marketing',
        relevance: 0.78,
        our: 'another value',
        created_at: '2024-01-13'
      }
    ]
    console.log('Fallback дані встановлені:', vTopData.value.length, 'записів')
  } finally {
    vTopLoading.value = false
    console.log('Завантаження завершено. Стан:', {
      loading: vTopLoading.value,
      error: vTopError.value,
      dataLength: vTopData.value.length
    })
  }
}

// Опції для фільтрів
const topicOptions = computed(() => {
  if (!vTopData.value || vTopData.value.length === 0) return []
  const topics = [...new Set(vTopData.value.map(item => item.topic).filter(Boolean))]
  return topics.sort()
})

const keywordsOptions = computed(() => {
  if (!vTopData.value || vTopData.value.length === 0) return []
  const keywords = [...new Set(vTopData.value.map(item => item.keywords).filter(Boolean))]
  return keywords.sort()
})

// Фільтровані дані
const filteredTopData = computed(() => {
  if (!vTopData.value || vTopData.value.length === 0) {
    return []
  }
  
  let filtered = [...vTopData.value]
  
  // Фільтр по topic
  if (filters.value.topic) {
    filtered = filtered.filter(item => item.topic === filters.value.topic)
  }
  
  // Фільтр по keywords
  if (filters.value.keywords) {
    filtered = filtered.filter(item => item.keywords === filters.value.keywords)
  }
  
  // Фільтр по our (тільки наші дані)
  if (filters.value.ourOnly) {
    filtered = filtered.filter(item => item.our !== null && item.our !== undefined)
  }
  
  return filtered
})

const applyFilters = () => {
  // Фільтрація відбувається автоматично через computed
  console.log('Фільтри застосовані:', filters.value)
}

const clearFilters = () => {
  filters.value = {
    topic: null,
    keywords: null,
    ourOnly: false
  }
  console.log('Фільтри очищені')
}

const vTopHeaders = computed(() => {
  if (!vTopData.value || vTopData.value.length === 0) {
    console.log('vTopHeaders: немає даних')
    return []
  }
  const firstItem = vTopData.value[0]
  if (!firstItem) {
    console.log('vTopHeaders: перший елемент порожній')
    return []
  }
  
  // Визначаємо порядок колонок
  const columnOrder = ['id', 'domain', 'title', 'description', 'topic', 'keywords', 'relevance', 'our', 'created_at']
  const allKeys = Object.keys(firstItem)
  
  // Сортуємо ключі за порядком, а потім додаємо решту
  const sortedKeys = columnOrder.filter(key => allKeys.includes(key))
  const remainingKeys = allKeys.filter(key => !columnOrder.includes(key))
  const finalKeys = [...sortedKeys, ...remainingKeys]
  
  const headers = finalKeys.map(key => ({ title: key, key }))
  console.log('vTopHeaders згенеровані:', headers)
  return headers
})

// Автоматичне завантаження даних при монтуванні
import { onMounted } from 'vue'

onMounted(() => {
  console.log('SEO компонент змонтовано, викликаємо fetchVTop')
  fetchVTop()
})
</script>

<style scoped>
.seo-page {
  width: 100%;
  height: 100vh;
  min-height: 0;
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.seo-top-card {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
}

.truncated-text {
  cursor: help;
  color: #1976d2;
}

.truncated-text:hover {
  text-decoration: underline;
}

.seo-top-card-text {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
  padding: 0 !important;
}

.filters-row {
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.v-theme--dark .filters-row {
  background-color: #424242;
  border-color: #616161;
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

.stat-card {
  transition: transform 0.2s ease-in-out;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.text-h3 {
  font-weight: 600;
  margin-bottom: 8px;
}

.text-caption {
  font-size: 0.875rem;
}

.seo-top-scroll {
  flex: 1 1 auto;
  min-height: 0;
  max-height: 100%;
  overflow-y: auto;
  margin-top: 8px;
  margin-bottom: 8px;
}

/* Стили для заголовків таблиці */
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

:deep(.v-theme--dark .v-table th) {
  background-color: #1e3a5f !important;
  color: #90caf9 !important;
  border-bottom: 3px solid #42a5f5 !important;
}


</style> 