<template>
  <div class="help-initializer">
    <v-card class="welcome-card">
      <v-card-title class="d-flex align-center">
        <v-icon size="large" class="mr-3">mdi-database-plus</v-icon>
        Инициализация базы данных Help
      </v-card-title>
      
      <v-card-text>
        <v-alert
          v-if="success"
          type="success"
          class="mb-4"
        >
          {{ success }}
        </v-alert>
        
        <v-alert
          v-if="error"
          type="error"
          class="mb-4"
        >
          {{ error }}
        </v-alert>
        
        <v-progress-circular
          v-if="loading"
          indeterminate
          color="primary"
          class="mb-4"
        ></v-progress-circular>
        
        <p class="text-body-1 mb-4">
          Этот компонент создаст начальные записи для всех разделов меню в базе данных.
          Нажмите кнопку "Инициализировать", чтобы создать записи.
        </p>
        
        <v-btn
          color="primary"
          size="large"
          @click="initializeHelpDatabase"
          :loading="loading"
          :disabled="loading"
          prepend-icon="mdi-database-plus"
        >
          Инициализировать базу данных Help
        </v-btn>
        
        <div v-if="initializedLinks.length > 0" class="mt-6">
          <h3 class="text-h6 mb-3">Созданные записи:</h3>
          <v-list>
            <v-list-item
              v-for="link in initializedLinks"
              :key="link.component"
              :prepend-icon="getIconForComponent(link.component)"
            >
              <v-list-item-title>{{ link.component }}</v-list-item-title>
              <v-list-item-subtitle>{{ link.url }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'

const loading = ref(false)
const error = ref(null)
const success = ref(null)
const initializedLinks = ref([])

// Начальные ссылки для всех разделов меню
const defaultHelpLinks = [
  { component: 'dashboard', url: 'https://dashboard.api4/docs/dashboard' },
  { component: 'finance', url: 'https://dashboard.api4/docs/finance' },
  { component: 'advertisement', url: 'https://dashboard.api4/docs/advertisement' },
  { component: 'seo', url: 'https://dashboard.api4/docs/seo' },
  { component: 'seo-top', url: 'https://dashboard.api4/docs/seo/top' },
  { component: 'seo-metatags', url: 'https://dashboard.api4/docs/seo/metatags' },
  { component: 'seo-metatags-gen', url: 'https://dashboard.api4/docs/seo/metatags-gen' },
  { component: 'market', url: 'https://dashboard.api4/docs/market' },
  { component: 'cp', url: 'https://dashboard.api4/docs/cp' },
  { component: 'projects', url: 'https://dashboard.api4/docs/projects' },
  { component: 'settings', url: 'https://dashboard.api4/docs/settings' },
  { component: 'currency-rates', url: 'https://dashboard.api4/docs/currency-rates' }
]

const getIconForComponent = (component) => {
  const iconMap = {
    'dashboard': 'mdi-view-dashboard',
    'finance': 'mdi-cash-multiple',
    'advertisement': 'mdi-google-ads',
    'seo': 'mdi-magnify',
    'seo-top': 'mdi-table',
    'seo-metatags': 'mdi-tag-multiple',
    'seo-metatags-gen': 'mdi-tag-multiple-check',
    'market': 'mdi-store',
    'cp': 'mdi-account-group',
    'projects': 'mdi-folder-multiple',
    'settings': 'mdi-cog',
    'currency-rates': 'mdi-currency-usd'
  }
  return iconMap[component] || 'mdi-help-circle'
}

const initializeHelpDatabase = async () => {
  loading.value = true
  error.value = null
  success.value = null
  initializedLinks.value = []
  
  try {
    // Сначала проверяем, есть ли уже записи
    const existingResponse = await axios.get(API_ENDPOINTS.HELP)
    const existingLinks = existingResponse.data || []
    
    if (existingLinks.length > 0) {
      // Если записи уже есть, обновляем их
      for (const link of defaultHelpLinks) {
        const existingLink = existingLinks.find(el => el.component === link.component)
        
        if (existingLink) {
          // Обновляем существующую запись
          await axios.patch(`${API_ENDPOINTS.HELP}?id=eq.${existingLink.id}`, {
            component: link.component,
            url: link.url
          })
        } else {
          // Создаем новую запись
          await axios.post(API_ENDPOINTS.HELP, {
            component: link.component,
            url: link.url
          })
        }
      }
      success.value = 'База данных Help успешно обновлена'
    } else {
      // Если записей нет, создаем все новые
      for (const link of defaultHelpLinks) {
        await axios.post(API_ENDPOINTS.HELP, {
          component: link.component,
          url: link.url
        })
      }
      success.value = 'База данных Help успешно инициализирована'
    }
    
    // Загружаем обновленные данные
    const updatedResponse = await axios.get(API_ENDPOINTS.HELP)
    initializedLinks.value = updatedResponse.data || []
    
    // Очистка сообщения об успехе через 5 секунд
    setTimeout(() => {
      success.value = null
    }, 5000)
    
  } catch (err) {
    error.value = 'Ошибка при инициализации: ' + (err.response?.data?.message || err.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.help-initializer {
  padding: 20px;
}

.welcome-card {
  max-width: 800px;
  margin: 0 auto;
}
</style>
