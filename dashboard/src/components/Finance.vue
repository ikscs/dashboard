<template>
  <div class="finance-container">
    <h2>Финансы</h2>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="finance-data">
      <div v-for="finance in finances" :key="finance.id" class="finance-item">
        <h3>{{ finance.name }}</h3>
        <p>Дата: {{ formatDate(finance.date) }}</p>
        <p>Сумма: {{ finance.amount }} ₽</p>
        <p>Категория: {{ finance.category }}</p>
      </div>
    </div>
    <div class="finance">
      <v-container fluid class="fill-height pa-0">
        <v-row no-gutters class="fill-height">
          <v-col cols="12" class="fill-height">
            <div class="content-wrapper">
              <v-row>
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
                    <v-card-text style="height: 400px">
                      <canvas ref="usdChart"></canvas>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>

              <v-row>
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
                    <v-card-text style="height: 400px">
                      <canvas ref="eurUsdChart"></canvas>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'Finance',
  data() {
    return {
      finances: [],
      loading: true,
      error: null,
      rates: [],
      usdChart: null,
      eurUsdChart: null,
      headers: [
        { 
          title: 'Дата',
          key: 'date',
          align: 'start'
        },
        { 
          title: 'НБУ',
          key: 'nbu',
          align: 'end'
        },
        { 
          title: 'Межбанк',
          key: 'interbank',
          align: 'end'
        },
        { 
          title: 'Наличный',
          key: 'cash',
          align: 'end'
        }
      ]
    }
  },
  computed: {
    pivotRates() {
      const usdRates = this.rates.filter(rate => rate.currency === 'USD')
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
    },
    eurUsdRates() {
      const dates = [...new Set(this.rates.map(rate => rate.date))].sort()
      
      return dates.map(date => {
        const dayRates = this.rates.filter(rate => rate.date === date)
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
    }
  },
  methods: {
    async fetchFinances() {
      try {
        const response = await axios.get('http://localhost:8000/api/finances/')
        this.finances = response.data
        this.loading = false
      } catch (error) {
        this.error = 'Ошибка при загрузке данных: ' + error.message
        this.loading = false
      }
    },
    async fetchRates() {
      try {
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(startDate.getDate() - 7)
        
        const response = await axios.get('http://localhost:8000/api/currency-rates/', {
          params: {
            date_after: this.formatDateForAPI(startDate),
            date_before: this.formatDateForAPI(endDate)
          }
        })
        this.rates = Array.isArray(response.data) ? response.data : []
        this.updateCharts()
      } catch (error) {
        console.error('Ошибка при загрузке курсов валют:', error)
        this.rates = []
      } finally {
        this.loading = false
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('ru-RU')
    },
    formatDateForAPI(date) {
      return date.toISOString().split('T')[0]
    },
    formatValue(value) {
      return value ? Number(value).toFixed(4) : '-'
    },
    updateCharts() {
      this.updateUsdChart()
      this.updateEurUsdChart()
    },
    updateUsdChart() {
      if (this.usdChart) {
        this.usdChart.destroy()
      }

      const datasets = [
        {
          label: 'НБУ',
          data: this.pivotRates.map(r => r.nbu),
          borderColor: '#FF6384',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Межбанк',
          data: this.pivotRates.map(r => r.interbank),
          borderColor: '#36A2EB',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Наличный',
          data: this.pivotRates.map(r => r.cash),
          borderColor: '#FFCE56',
          fill: false,
          spanGaps: true,
          tension: 0.1
        }
      ]

      const ctx = this.$refs.usdChart.getContext('2d')
      this.usdChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.pivotRates.map(r => this.formatDate(r.date)),
          datasets
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Динамика курсов USD'
            }
          },
          scales: {
            y: {
              beginAtZero: false
            }
          },
          elements: {
            line: {
              tension: 0.1
            }
          }
        }
      })
    },
    updateEurUsdChart() {
      if (this.eurUsdChart) {
        this.eurUsdChart.destroy()
      }

      const datasets = [
        {
          label: 'НБУ',
          data: this.eurUsdRates.map(r => r.nbu),
          borderColor: '#FF6384',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Межбанк',
          data: this.eurUsdRates.map(r => r.interbank),
          borderColor: '#36A2EB',
          fill: false,
          spanGaps: true,
          tension: 0.1
        },
        {
          label: 'Наличный',
          data: this.eurUsdRates.map(r => r.cash),
          borderColor: '#FFCE56',
          fill: false,
          spanGaps: true,
          tension: 0.1
        }
      ]

      const ctx = this.$refs.eurUsdChart.getContext('2d')
      this.eurUsdChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.eurUsdRates.map(r => this.formatDate(r.date)),
          datasets
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'Динамика курсов EUR/USD'
            }
          },
          scales: {
            y: {
              beginAtZero: false
            }
          },
          elements: {
            line: {
              tension: 0.1
            }
          }
        }
      })
    }
  },
  mounted() {
    this.fetchFinances()
    this.fetchRates()
  },
  beforeUnmount() {
    if (this.usdChart) {
      this.usdChart.destroy()
    }
    if (this.eurUsdChart) {
      this.eurUsdChart.destroy()
    }
  }
}
</script>

<style scoped>
.finance-container {
  padding: 20px;
  width: 100%;
  text-align: left;
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

.finance-data {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.finance-item {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.finance-item h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.finance-item p {
  margin: 5px 0;
  color: #666;
}

.finance {
  height: 100vh;
  overflow: hidden;
  width: 100%;
}

.content-wrapper {
  height: calc(100vh - 64px);
  overflow-y: auto;
  padding: 20px;
  width: 100%;
}

.v-container {
  max-width: 100% !important;
  padding: 0 !important;
}

.v-row {
  margin: 0 !important;
  width: 100%;
}

.table-wrapper {
  height: 400px;
  overflow-y: auto;
  position: relative;
}

.currency-table {
  width: 100%;
  border-collapse: collapse;
}

.currency-table th {
  background-color: #f5f5f5;
  font-weight: bold;
  color: #000;
  padding: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  position: sticky;
  top: 0;
  z-index: 1;
}

.currency-table td {
  padding: 8px 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  background-color: white;
}

.currency-table tr:last-child td {
  border-bottom: none;
}

.v-card {
  margin-bottom: 20px;
  height: 500px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.v-card-text {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.v-card-text > div {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.v-card-text canvas {
  max-height: 100%;
}
</style> 