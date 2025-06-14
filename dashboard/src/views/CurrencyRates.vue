<template>
  <div class="currency-rates">
    <v-card>
      <v-card-title>
        Курсы валют
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Поиск"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="rates"
        :search="search"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.date="{ item }">
          {{ formatDate(item.date) }}
        </template>
        <template v-slot:item.type="{ item }">
          {{ item.type_display }}
        </template>
        <template v-slot:item.value="{ item }">
          {{ formatValue(item.value) }}
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CurrencyRates',
  data() {
    return {
      search: '',
      loading: true,
      rates: [],
      headers: [
        { text: 'Дата', value: 'date', align: 'start' },
        { text: 'Валюта', value: 'currency', align: 'start' },
        { text: 'Тип', value: 'type', align: 'start' },
        { text: 'Значение', value: 'value', align: 'end' }
      ]
    }
  },
  methods: {
    async fetchRates() {
      try {
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(startDate.getDate() - 7)
        
        const response = await axios.get('/api/currency-rates/', {
          params: {
            date_after: this.formatDateForAPI(startDate),
            date_before: this.formatDateForAPI(endDate)
          }
        })
        this.rates = response.data
      } catch (error) {
        console.error('Ошибка при загрузке курсов валют:', error)
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
      return Number(value).toFixed(4)
    }
  },
  mounted() {
    this.fetchRates()
  }
}
</script>

<style scoped>
.currency-rates {
  padding: 20px;
}
</style> 