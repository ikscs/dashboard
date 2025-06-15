<template>
  <div class="finance">
    <v-container fluid>
      <v-row>
        <!-- Первая линия -->
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>Курсы USD</v-card-title>
            <div class="table-wrapper">
              <table class="currency-table">
                <thead>
                  <tr>
                    <th class="text-start">Дата</th>
                    <th class="text-end">НБУ</th>
                    <th class="text-end">Межбанк</th>
                    <th class="text-end">Наличный</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in pivotRates" :key="item.date">
                    <td>{{ formatDate(item.date) }}</td>
                    <td class="text-end">{{ formatValue(item.nbu) }}</td>
                    <td class="text-end">{{ formatValue(item.interbank) }}</td>
                    <td class="text-end">{{ formatValue(item.cash) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>График курсов USD</v-card-title>
            <v-card-text>
              <canvas id="usdChart"></canvas>
            </v-card-text>
          </v-card>
        </v-col>
        
        <!-- Вторая линия -->
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>Курсы EUR/USD</v-card-title>
            <div class="table-wrapper">
              <table class="currency-table">
                <thead>
                  <tr>
                    <th class="text-start">Дата</th>
                    <th class="text-end">НБУ</th>
                    <th class="text-end">Межбанк</th>
                    <th class="text-end">Наличный</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in eurUsdRates" :key="item.date">
                    <td>{{ formatDate(item.date) }}</td>
                    <td class="text-end">{{ formatValue(item.nbu) }}</td>
                    <td class="text-end">{{ formatValue(item.interbank) }}</td>
                    <td class="text-end">{{ formatValue(item.cash) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>График курсов EUR/USD</v-card-title>
            <v-card-text>
              <canvas id="eurUsdChart"></canvas>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'
import { API_ENDPOINTS } from '../config/api'

const finances = ref([])
const loading = ref(true)
const error = ref(null)
const rates = ref([])
const usdChart = ref(null)
const eurUsdChart = ref(null)

const pivotRates = computed(() => {
  const usdRates = rates.value.filter(rate => rate.currency === 'USD')
  const dates = [...new Set(usdRates.map(rate => rate.date))].sort()
  
  return dates.map(date => {
    const dayRates = usdRates.filter(rate => rate.date === date)
    return {
      date,
      nbu: dayRates.find(r => r.type === '0')?.value || null,
      interbank: dayRates.find(r => r.type === '1')?.value || null,
      cash: dayRates.find(r => r.type === '2')?.value || null
    }
  })
})

const eurUsdRates = computed(() => {
  const dates = [...new Set(rates.value.map(rate => rate.date))].sort()
  
  return dates.map(date => {
    const dayRates = rates.value.filter(rate => rate.date === date)
    const eurRates = dayRates.filter(r => r.currency === 'EUR')
    const usdRates = dayRates.filter(r => r.currency === 'USD')
    
    const calculateRatio = (eurType, usdType) => {
      const eurRate = eurRates.find(r => r.type === eurType)?.value
      const usdRate = usdRates.find(r => r.type === usdType)?.value
      return eurRate && usdRate ? (eurRate / usdRate) : null
    }
    
    return {
      date,
      nbu: calculateRatio('0', '0'),
      interbank: calculateRatio('1', '1'),
      cash: calculateRatio('2', '2')
    }
  })
})

const fetchFinances = async () => {
  try {
    const response = await axios.get(API_ENDPOINTS.FINANCES)
    finances.value = response.data
    loading.value = false
  } catch (error) {
    error.value = 'Ошибка при загрузке данных: ' + error.message
    loading.value = false
  }
}

const fetchRates = async () => {
  try {
    const endDate = new Date()
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - 7) // Получаем данные за последние 7 дней

    const response = await axios.get(API_ENDPOINTS.CURRENCY_RATES, {
      params: {
        date_after: formatDateForAPI(startDate),
        date_before: formatDateForAPI(endDate)
      }
    })
    rates.value = Array.isArray(response.data) ? response.data : []
    updateCharts()
  } catch (error) {
    console.error('Ошибка при загрузке курсов валют:', error)
    rates.value = []
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ru-RU')
}

const formatDateForAPI = (date) => {
  return date.toISOString().split('T')[0]
}

const formatValue = (value) => {
  return value ? Number(value).toFixed(4) : '-'
}

const updateCharts = () => {
  updateUsdChart()
  updateEurUsdChart()
}

const updateUsdChart = () => {
  if (usdChart.value) {
    usdChart.value.destroy()
  }

  const ctx = document.getElementById('usdChart')
  if (!ctx) return

  usdChart.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: pivotRates.value.map(r => formatDate(r.date)),
      datasets: [
        {
          label: 'НБУ',
          data: pivotRates.value.map(r => r.nbu),
          borderColor: '#FF6384',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Межбанк',
          data: pivotRates.value.map(r => r.interbank),
          borderColor: '#36A2EB',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Наличный',
          data: pivotRates.value.map(r => r.cash),
          borderColor: '#4CAF50',
          fill: false,
          spanGaps: true,
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          align: 'start',
          labels: {
            boxWidth: 12,
            padding: 15
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: {
            callback: function(value) {
              return value.toFixed(2)
            }
          }
        }
      }
    }
  })
}

const updateEurUsdChart = () => {
  if (eurUsdChart.value) {
    eurUsdChart.value.destroy()
  }

  const ctx = document.getElementById('eurUsdChart')
  if (!ctx) return

  eurUsdChart.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: eurUsdRates.value.map(r => formatDate(r.date)),
      datasets: [
        {
          label: 'НБУ',
          data: eurUsdRates.value.map(r => r.nbu),
          borderColor: '#FF6384',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Межбанк',
          data: eurUsdRates.value.map(r => r.interbank),
          borderColor: '#36A2EB',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Наличный',
          data: eurUsdRates.value.map(r => r.cash),
          borderColor: '#4CAF50',
          fill: false,
          spanGaps: true,
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          align: 'start',
          labels: {
            boxWidth: 12,
            padding: 15
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: {
            callback: function(value) {
              return value.toFixed(4)
            }
          }
        }
      }
    }
  })
}

onMounted(() => {
  fetchFinances()
  fetchRates()
})

onBeforeUnmount(() => {
  if (usdChart.value) {
    usdChart.value.destroy()
  }
  if (eurUsdChart.value) {
    eurUsdChart.value.destroy()
  }
})
</script>

<style scoped>
.finance {
  padding: 20px;
  height: calc(100vh - 64px);
  box-sizing: border-box;
  display: grid;
  grid-template-rows: 1fr 1fr;
  gap: 24px;
}

.v-container {
  height: 100%;
  padding: 0 !important;
  margin-bottom: 0;
}

.v-row {
  margin: 0;
  height: 100%;
}

.v-col {
  padding: 8px;
}

.table-wrapper {
  height: 100%;
  overflow-y: auto;
  position: relative;
  margin: 0 -16px;
  padding: 0 16px;
}

.currency-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.currency-table th {
  background-color: rgb(var(--v-theme-surface));
  font-weight: bold;
  color: rgb(var(--v-theme-on-surface));
  padding: 8px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  position: sticky;
  top: 0;
  z-index: 1;
}

.currency-table td {
  padding: 6px 8px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  background-color: rgb(var(--v-theme-surface));
  color: rgb(var(--v-theme-on-surface));
}

.currency-table tr:last-child td {
  border-bottom: none;
}

.currency-table tbody tr:hover {
  background-color: rgba(var(--v-theme-surface-variant), 0.1);
}

.v-card {
  height: 100%;
  margin: 0;
  background-color: rgb(var(--v-theme-surface)) !important;
  display: flex;
  flex-direction: column;
}

.v-card-text {
  flex: 1;
  padding: 8px !important;
  display: flex;
  flex-direction: column;
}

.v-card-text canvas {
  flex: 1;
  width: 100%;
  height: 100%;
  margin-top: 20px;
}

.v-card-title {
  padding: 12px !important;
  font-size: 1rem !important;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  flex-shrink: 0;
}
</style> 