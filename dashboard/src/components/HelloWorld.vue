<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'

const message = ref('Загрузка...')
const error = ref(null)
const loading = ref(false)
const latestRates = ref(null)
const previousRates = ref(null)
const rateDates = ref({
  nbu: null,
  interbank: null,
  cash: null
})
const rateChanges = ref({
  nbu: { value: null, percent: null, trend: '' },
  interbank: { value: null, percent: null, trend: '' },
  cash: { value: null, percent: null, trend: '' }
})

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

const fetchAdStats = async () => {
  try {
    const response = await axios.get(API_ENDPOINTS.ADVERTISEMENT)
    const data = Array.isArray(response.data) ? response.data : []
    adStats.value = data
    if (data.length > 0) {
      // Сортируем по дате по убыванию
      const sorted = [...data].sort((a, b) => new Date(b.date) - new Date(a.date))
      const latest = sorted[0]
      const prev = sorted[1] || {}
      adSummary.value = {
        show: latest.show ?? latest.total_views ?? null,
        click: latest.click ?? latest.total_clicks ?? null,
        ctr: latest.ctr ?? null,
        date: latest.date ?? null
      }
      adPrevSummary.value = {
        show: prev.show ?? prev.total_views ?? null,
        click: prev.click ?? prev.total_clicks ?? null,
        ctr: prev.ctr ?? null,
        date: prev.date ?? null
      }
      adDiff.value = {
        show: adSummary.value.show !== null && adPrevSummary.value.show !== null ? adSummary.value.show - adPrevSummary.value.show : null,
        click: adSummary.value.click !== null && adPrevSummary.value.click !== null ? adSummary.value.click - adPrevSummary.value.click : null,
        ctr: adSummary.value.ctr !== null && adPrevSummary.value.ctr !== null ? adSummary.value.ctr - adPrevSummary.value.ctr : null
      }
    }
  } catch (err) {
    // Не критично для дашборда
    adStats.value = []
    adSummary.value = { show: null, click: null, ctr: null, date: null }
    adPrevSummary.value = { show: null, click: null, ctr: null, date: null }
    adDiff.value = { show: null, click: null, ctr: null }
  }
}

const formatAdValue = (value, digits = 0) => {
  if (value === null || value === undefined) return '-'
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: digits })
}
const formatAdPercent = (value) => {
  if (value === null || value === undefined) return '-'
  return (value * 100).toFixed(2) + '%'
}
const formatAdDiff = (value, digits = 0, isPercent = false) => {
  if (value === null || value === undefined) return ''
  const sign = value > 0 ? '+' : value < 0 ? '' : ''
  const color = value > 0 ? 'ad-green' : value < 0 ? 'ad-red' : ''
  let formatted = isPercent ? (value * 100).toFixed(2) + '%' : Math.abs(value).toLocaleString('ru-RU', { maximumFractionDigits: digits })
  return `<span class="${color}">${sign}${formatted}</span>`
}

// --- Валюты ---
const fetchMessage = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await axios.get(API_ENDPOINTS.HELLO)
    message.value = response.data.message
  } catch (err) {
    error.value = 'Ошибка при загрузке данных: ' + err.message
    message.value = 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

const fetchCurrencyRates = async () => {
  try {
    const response = await axios.get(API_ENDPOINTS.CURRENCY_RATES)
    const allRates = Array.isArray(response.data) ? response.data : []

    if (allRates.length === 0) {
      console.warn('Нет данных о курсах валют')
      return
    }

    const usdRates = allRates.filter(rate => rate.currency === 'USD')

    // Получаем крайние даты для каждого типа курса
    const nbuRates = usdRates.filter(rate => rate.type === '0').sort((a, b) => new Date(b.date) - new Date(a.date))
    const interbankRates = usdRates.filter(rate => rate.type === '1').sort((a, b) => new Date(b.date) - new Date(a.date))
    const cashRates = usdRates.filter(rate => rate.type === '2').sort((a, b) => new Date(b.date) - new Date(a.date))

    // Получаем данные за крайние даты
    const latestNbu = nbuRates[0]
    const latestInterbank = interbankRates[0]
    const latestCash = cashRates[0]

    // Получаем предыдущие данные для расчета изменений
    const previousNbu = nbuRates[1]
    const previousInterbank = interbankRates[1]
    const previousCash = cashRates[1]

    latestRates.value = {
      nbu: latestNbu?.value || null,
      interbank: latestInterbank?.value || null,
      cash: latestCash?.value || null
    }

    previousRates.value = {
      nbu: previousNbu?.value || null,
      interbank: previousInterbank?.value || null,
      cash: previousCash?.value || null
    }

    // Сохраняем даты
    rateDates.value = {
      nbu: latestNbu?.date || null,
      interbank: latestInterbank?.date || null,
      cash: latestCash?.date || null
    }

    // Расчет изменений
    const calculateChange = (latest, previous) => {
      if (latest === null || previous === null) return { value: null, percent: null, trend: '' }
      const diff = latest - previous
      const percent = (diff / previous) * 100
      // Инвертируем тренд, так как для валюты рост курса - это падение значения
      const trend = diff < 0 ? 'up' : diff > 0 ? 'down' : 'neutral'
      return { value: Math.abs(diff), percent: Math.abs(percent), trend: trend }
    }

    rateChanges.value.nbu = calculateChange(latestRates.value.nbu, previousRates.value.nbu)
    rateChanges.value.interbank = calculateChange(latestRates.value.interbank, previousRates.value.interbank)
    rateChanges.value.cash = calculateChange(latestRates.value.cash, previousRates.value.cash)
  } catch (err) {
    console.error('Ошибка при загрузке курсов валют:', err)
    error.value = 'Ошибка при загрузке курсов валют: ' + err.message
  }
}

const formatValue = (value) => {
  return value ? Number(value).toFixed(4) : '-'
}

const formatChangeValue = (value) => {
  if (value === null) return '-'
  return Math.abs(value).toFixed(2)
}

const formatChangePercent = (value) => {
  if (value === null) return '-'
  return Math.abs(value).toFixed(2) + '%'
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU')
}

onMounted(() => {
  fetchMessage()
  fetchCurrencyRates()
  fetchAdStats()
})
</script>

<template>
  <div class="hello-world-row">
    <div class="hello-world">
      <h1>{{ message }}</h1>
      <p v-if="error" class="error">{{ error }}</p>
      
      <div v-if="latestRates" class="currency-display">
        <div class="currency-item">
          <div class="currency-label">НБУ</div>
          <div class="currency-value">{{ formatValue(latestRates.nbu) }}</div>
          <div :class="['currency-change', rateChanges.nbu.trend]">
            <span v-if="rateChanges.nbu.trend === 'down'">&#9650;</span>
            <span v-if="rateChanges.nbu.trend === 'up'">&#9660;</span>
            {{ formatChangePercent(rateChanges.nbu.percent) }} ({{ formatChangeValue(rateChanges.nbu.value) }})
          </div>
          <div class="currency-date">{{ formatDate(rateDates.nbu) }}</div>
        </div>
        <div class="currency-item">
          <div class="currency-label">Межбанк</div>
          <div class="currency-value">{{ formatValue(latestRates.interbank) }}</div>
          <div :class="['currency-change', rateChanges.interbank.trend]">
            <span v-if="rateChanges.interbank.trend === 'down'">&#9650;</span>
            <span v-if="rateChanges.interbank.trend === 'up'">&#9660;</span>
            {{ formatChangePercent(rateChanges.interbank.percent) }} ({{ formatChangeValue(rateChanges.interbank.value) }})
          </div>
          <div class="currency-date">{{ formatDate(rateDates.interbank) }}</div>
        </div>
        <div class="currency-item">
          <div class="currency-label">Наличный</div>
          <div class="currency-value">{{ formatValue(latestRates.cash) }}</div>
          <div :class="['currency-change', rateChanges.cash.trend]">
            <span v-if="rateChanges.cash.trend === 'down'">&#9650;</span>
            <span v-if="rateChanges.cash.trend === 'up'">&#9660;</span>
            {{ formatChangePercent(rateChanges.cash.percent) }} ({{ formatChangeValue(rateChanges.cash.value) }})
          </div>
          <div class="currency-date">{{ formatDate(rateDates.cash) }}</div>
        </div>
      </div>

      <v-btn
        color="primary"
        @click="fetchMessage"
        :loading="loading"
        class="mt-4"
      >
        Обновить сообщение
      </v-btn>
    </div>
    <div class="ad-summary-block">
      <h2 class="ad-summary-title">Реклама ({{ formatDate(adSummary.date) }})</h2>
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
  </div>
</template>

<style scoped>
.hello-world-row {
  display: flex;
  flex-direction: row;
  gap: 32px;
  justify-content: center;
  align-items: flex-start;
}
.hello-world {
  text-align: center;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  margin: 2rem auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  min-width: 320px;
  flex: 1 1 320px;
}
.currency-display {
  display: flex;
  justify-content: space-around;
  margin-top: 2rem;
  flex-wrap: wrap;
}
.currency-item {
  flex: 1;
  min-width: 150px;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  margin: 0.5rem;
  text-align: center;
}
.currency-label {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 0.5rem;
}
.currency-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}
.currency-change {
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-bottom: 0.5rem;
}
.currency-date {
  font-size: 0.75rem;
  color: #888;
  font-style: italic;
}
.currency-change.up {
  color: #4CAF50;
}
.currency-change.down {
  color: #F44336;
}
.currency-change.up span {
  color: #4CAF50;
}
.currency-change.down span {
  color: #F44336;
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

/* --- Рекламная сводка --- */
.ad-summary-block {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  min-width: 260px;
  max-width: 340px;
  flex: 1 1 260px;
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.ad-summary-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  color: #2c3e50;
}
.ad-summary-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  margin-bottom: 0.7rem;
}
.ad-summary-label {
  color: #555;
  min-width: 70px;
}
.ad-summary-value {
  font-weight: 600;
  color: #2c3e50;
  min-width: 60px;
  text-align: right;
}
.ad-summary-date {
  font-size: 0.85rem;
  color: #888;
  margin-top: 1.2rem;
  font-style: italic;
}
.ad-green {
  color: #4CAF50;
  font-weight: 600;
  margin-left: 6px;
}
.ad-red {
  color: #F44336;
  font-weight: 600;
  margin-left: 6px;
}
@media (max-width: 900px) {
  .hello-world-row {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  .hello-world, .ad-summary-block {
    margin: 1rem auto;
    max-width: 100%;
  }
}
</style>
