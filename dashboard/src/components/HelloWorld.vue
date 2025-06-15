<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'

const message = ref('Загрузка...')
const error = ref(null)
const loading = ref(false)
const latestRates = ref(null)
const previousRates = ref(null)
const rateChanges = ref({
  nbu: { value: null, percent: null, trend: '' },
  interbank: { value: null, percent: null, trend: '' },
  cash: { value: null, percent: null, trend: '' }
})

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

    // Сортируем по дате, чтобы получить последние две записи
    const sortedRates = usdRates.sort((a, b) => new Date(b.date) - new Date(a.date))

    if (sortedRates.length >= 2) {
      const latestDate = sortedRates[0].date
      const previousDate = sortedRates.find(rate => rate.date !== latestDate)?.date

      if (previousDate) {
        latestRates.value = {
          nbu: sortedRates.find(r => r.date === latestDate && r.type === '0')?.value,
          interbank: sortedRates.find(r => r.date === latestDate && r.type === '1')?.value,
          cash: sortedRates.find(r => r.date === latestDate && r.type === '2')?.value
        }

        previousRates.value = {
          nbu: sortedRates.find(r => r.date === previousDate && r.type === '0')?.value,
          interbank: sortedRates.find(r => r.date === previousDate && r.type === '1')?.value,
          cash: sortedRates.find(r => r.date === previousDate && r.type === '2')?.value
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
      }
    }
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

onMounted(() => {
  fetchMessage()
  fetchCurrencyRates()
})
</script>

<template>
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
      </div>
      <div class="currency-item">
        <div class="currency-label">Межбанк</div>
        <div class="currency-value">{{ formatValue(latestRates.interbank) }}</div>
        <div :class="['currency-change', rateChanges.interbank.trend]">
          <span v-if="rateChanges.interbank.trend === 'down'">&#9650;</span>
          <span v-if="rateChanges.interbank.trend === 'up'">&#9660;</span>
          {{ formatChangePercent(rateChanges.interbank.percent) }} ({{ formatChangeValue(rateChanges.interbank.value) }})
        </div>
      </div>
      <div class="currency-item">
        <div class="currency-label">Наличный</div>
        <div class="currency-value">{{ formatValue(latestRates.cash) }}</div>
        <div :class="['currency-change', rateChanges.cash.trend]">
          <span v-if="rateChanges.cash.trend === 'down'">&#9650;</span>
          <span v-if="rateChanges.cash.trend === 'up'">&#9660;</span>
          {{ formatChangePercent(rateChanges.cash.percent) }} ({{ formatChangeValue(rateChanges.cash.value) }})
        </div>
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
</template>

<style scoped>
.hello-world {
  text-align: center;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  margin: 2rem auto; /* Центрируем по горизонтали */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 800px; /* Ограничиваем ширину */
}

.currency-display {
  display: flex;
  justify-content: space-around;
  margin-top: 2rem;
  flex-wrap: wrap; /* Позволяет элементам переноситься на новую строку */
}

.currency-item {
  flex: 1;
  min-width: 150px; /* Минимальная ширина для элемента */
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
}

.currency-change.up {
  color: #4CAF50; /* Зеленый для роста */
}

.currency-change.down {
  color: #F44336; /* Красный для падения */
}

.currency-change.up span {
  color: #4CAF50; /* Зеленый для треугольника при росте */
}

.currency-change.down span {
  color: #F44336; /* Красный для треугольника при падении */
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
