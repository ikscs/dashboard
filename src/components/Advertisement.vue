<template>
  <div class="advertisement-page">
    <!-- Блок краткой статистики рекламы -->
    <v-card class="welcome-card mb-6">
      <v-card-title class="d-flex align-center">
        <v-icon size="large" class="mr-3">mdi-google-ads</v-icon>
        Реклама ({{ formatDate(adSummary.date) }})
      </v-card-title>
      
      <v-card-text>
        <div v-if="!adSummary.date && !adLoading" class="text-center py-8">
          <v-icon color="grey" class="mr-2">mdi-chart-line</v-icon>
          Немає даних реклами
        </div>
        
        <div v-else class="ad-summary-content">
          <div class="ad-summary-row">
            <span class="ad-summary-label">Показы:</span>
            <span class="ad-summary-value">{{ formatAdValue(adSummary.show) }}</span>
            <span v-html="formatAdDiff(adDiff.show)"></span>
          </div>
          <div class="ad-summary-row">
            <span class="ad-summary-label">Клики:</span>
            <span class="ad-summary-value">{{ formatAdValue(adSummary.click) }}</span>
            <span v-html="formatAdDiff(adDiff.click)"></span>
          </div>
          <div class="ad-summary-row">
            <span class="ad-summary-label">CTR:</span>
            <span class="ad-summary-value">{{ formatAdPercent(adSummary.ctr) }}</span>
            <span v-html="formatAdDiff(adDiff.ctr, 2, true)"></span>
          </div>
          <div class="ad-summary-date">Сравнение с {{ formatDate(adPrevSummary.date) }}</div>
        </div>
      </v-card-text>
    </v-card>

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
import { API_ENDPOINTS, API_HEADERS } from '../config/api'

// --- Рекламная статистика ---
const adStats = ref([])
const adSummary = ref({
  show: null,
  click: null,
  ctr: null,
  date: null
})
const adPrevSummary = ref({
  show: null,
  click: null,
  ctr: null,
  date: null
})
const adDiff = ref({
  show: null,
  click: null,
  ctr: null
})
const adLoading = ref(false)

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

// Функция форматирования даты
const formatDate = (dateString) => {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('uk-UA', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit' 
    })
  } catch {
    return dateString
  }
}

// Функции форматирования рекламных данных
const formatAdValue = (value, digits = 0) => {
  if (value === null || value === undefined) return '—'
  return new Intl.NumberFormat('uk-UA', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  }).format(value)
}

const formatAdPercent = (value) => {
  if (value === null || value === undefined) return '—'
  return (value * 100).toFixed(2) + '%'
}

const formatAdDiff = (value, digits = 0, isPercent = false) => {
  if (value === null || value === undefined) return ''
  const sign = value >= 0 ? '+' : ''
  const formatted = isPercent 
    ? (value * 100).toFixed(digits) + '%'
    : new Intl.NumberFormat('uk-UA', {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits
      }).format(value)
  const color = value >= 0 ? 'green' : 'red'
  return ` <span style="color: ${color}">(${sign}${formatted})</span>`
}

// Загрузка рекламной статистики
const fetchAdStats = async () => {
  adLoading.value = true
  try {
    console.log('Запрос к ADVERTISEMENT:', API_ENDPOINTS.ADVERTISEMENT)
    console.log('Заголовки:', API_HEADERS.ADV)
    
    const response = await axios.get(API_ENDPOINTS.ADVERTISEMENT, {
      headers: API_HEADERS.ADV
    })
    
    console.log('Ответ API:', response.status, response.data)
    
    // Обработка разных форматов ответа
    let data = []
    if (Array.isArray(response.data)) {
      data = response.data
    } else if (response.data && typeof response.data === 'object') {
      if (Array.isArray(response.data.data)) {
        data = response.data.data
      } else if (Array.isArray(response.data.results)) {
        data = response.data.results
      } else {
        data = [response.data]
      }
    }
    
    adStats.value = data
    
    if (data.length > 0) {
      const sorted = [...data].sort((a, b) => {
        const dateA = new Date(a.date || a.date_created || a.created_at || 0)
        const dateB = new Date(b.date || b.date_created || b.created_at || 0)
        return dateB - dateA
      })
      
      const latest = sorted[0]
      const prev = sorted[1] || {}
      
      adSummary.value = {
        show: latest.show ?? latest.total_views ?? latest.views ?? latest.impressions ?? null,
        click: latest.click ?? latest.total_clicks ?? latest.clicks ?? null,
        ctr: latest.ctr ?? (latest.click && latest.show ? latest.click / latest.show : null),
        date: latest.date ?? latest.date_created ?? latest.created_at ?? null
      }
      
      adPrevSummary.value = {
        show: prev.show ?? prev.total_views ?? prev.views ?? prev.impressions ?? null,
        click: prev.click ?? prev.total_clicks ?? prev.clicks ?? null,
        ctr: prev.ctr ?? (prev.click && prev.show ? prev.click / prev.show : null),
        date: prev.date ?? prev.date_created ?? prev.created_at ?? null
      }
      
      adDiff.value = {
        show: adSummary.value.show !== null && adPrevSummary.value.show !== null ? adSummary.value.show - adPrevSummary.value.show : null,
        click: adSummary.value.click !== null && adPrevSummary.value.click !== null ? adSummary.value.click - adPrevSummary.value.click : null,
        ctr: adSummary.value.ctr !== null && adPrevSummary.value.ctr !== null ? adSummary.value.ctr - adPrevSummary.value.ctr : null
      }
    } else {
      adSummary.value = { show: null, click: null, ctr: null, date: null }
      adPrevSummary.value = { show: null, click: null, ctr: null, date: null }
      adDiff.value = { show: null, click: null, ctr: null }
    }
  } catch (err) {
    console.error('Ошибка при загрузке рекламы:', err)
    adStats.value = []
    adSummary.value = { show: null, click: null, ctr: null, date: null }
    adPrevSummary.value = { show: null, click: null, ctr: null, date: null }
    adDiff.value = { show: null, click: null, ctr: null }
  } finally {
    adLoading.value = false
  }
}

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
    const response = await axios.get(API_ENDPOINTS.ADVERTISEMENT, {
      headers: API_HEADERS.ADV
    })
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
  fetchAdStats() // Добавьте вызов
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

.ad-summary-content {
  padding: 16px 0;
}

.ad-summary-row {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(var(--v-theme-outline), 0.12);
}

.ad-summary-row:last-of-type {
  border-bottom: none;
}

.ad-summary-label {
  font-weight: 600;
  min-width: 120px;
  color: rgba(var(--v-theme-on-surface), 0.87);
}

.ad-summary-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: rgba(var(--v-theme-primary), 1);
  margin-left: 16px;
  margin-right: 8px;
}

.ad-summary-date {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(var(--v-theme-outline), 0.12);
  font-size: 0.875rem;
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-style: italic;
}
</style> 