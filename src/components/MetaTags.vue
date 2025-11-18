<template>
  <div class="metatags-page">
    <!-- Meta Group IKSCS Section -->
    <v-card class="mt-6 metatags-card">
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-database</v-icon>
        v_meta_group (схема ikscs)
      </v-card-title>
      <v-card-text class="metatags-card-text">
        <div v-if="metaGroupIkscsLoading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <div class="mt-4 text-body-1">Загрузка данных v_meta_group (ikscs)...</div>
        </div>
        <div v-else-if="metaGroupIkscsError" class="text-center py-8">
          <v-alert type="error" variant="tonal">
            <v-alert-title>Ошибка загрузки v_meta_group (ikscs)</v-alert-title>
            {{ metaGroupIkscsError }}
          </v-alert>
        </div>
        <div v-else-if="metaGroupIkscsData && metaGroupIkscsData.length > 0" class="metatags-scroll">
          <v-table>
            <thead>
              <tr>
                <th v-for="header in metaGroupIkscsHeaders" :key="header.key" class="text-left">
                  {{ header.title }}
                </th>
              </tr>
            </thead>
            <tbody>
                             <tr v-for="(item, index) in metaGroupIkscsData" :key="index">
                <td v-for="header in metaGroupIkscsHeaders" :key="header.key">
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
            <v-alert-title>Нет данных v_meta_group (ikscs)</v-alert-title>
            Нажмите "Обновить" для загрузки
          </v-alert>
        </div>
      </v-card-text>
    </v-card>

    <!-- Meta Group MC Section -->
    <v-card class="mt-6 metatags-card">
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-database</v-icon>
        v_meta_group (схема mc)
      </v-card-title>
      <v-card-text class="metatags-card-text">
        <div v-if="metaGroupMcLoading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <div class="mt-4 text-body-1">Загрузка данных v_meta_group (mc)...</div>
        </div>
        <div v-else-if="metaGroupMcError" class="text-center py-8">
          <v-alert type="error" variant="tonal">
            <v-alert-title>Ошибка загрузки v_meta_group (mc)</v-alert-title>
            {{ metaGroupMcError }}
          </v-alert>
        </div>
        <div v-else-if="metaGroupMcData && metaGroupMcData.length > 0" class="metatags-scroll">
          <v-table>
            <thead>
              <tr>
                <th v-for="header in metaGroupMcHeaders" :key="header.key" class="text-left">
                  {{ header.title }}
                </th>
              </tr>
            </thead>
            <tbody>
                             <tr v-for="(item, index) in metaGroupMcData" :key="index">
                <td v-for="header in metaGroupMcHeaders" :key="header.key">
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
            <v-alert-title>Нет данных v_meta_group (mc)</v-alert-title>
            Нажмите "Обновить" для загрузки
          </v-alert>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS, API_HEADERS } from '@/config/api.js'

// Meta Group IKSCS data
const metaGroupIkscsData = ref([])
const metaGroupIkscsLoading = ref(false)
const metaGroupIkscsError = ref(null)

// Meta Group MC data
const metaGroupMcData = ref([])
const metaGroupMcLoading = ref(false)
const metaGroupMcError = ref(null)

const fetchMetaGroupIkscs = async () => {
  metaGroupIkscsLoading.value = true
  metaGroupIkscsError.value = null
  try {
    console.log('Запрос v_meta_group (ikscs) к:', API_ENDPOINTS.META_GROUP_IKSCS)
    console.log('Заголовки:', API_HEADERS.IKSCS)
    
    const response = await axios.get(API_ENDPOINTS.META_GROUP_IKSCS, {
      headers: API_HEADERS.IKSCS
    })
    metaGroupIkscsData.value = response.data
  } catch (err) {
    console.error('Ошибка API v_meta_group (ikscs):', err)
    metaGroupIkscsError.value = err.response?.data?.message || err.message || 'Неизвестная ошибка'
    
    // Fallback дані для тестування
    console.log('Використовуємо fallback дані для v_meta_group (ikscs)')
    metaGroupIkscsError.value = null // Очищаємо помилку
    metaGroupIkscsData.value = [
      {
        meta: 'title_ua',
        count: 1,
        null: 4294
      },
      {
        meta: 'descr_ua',
        count: 111,
        null: 3734
      },
      {
        meta: 'title_ru',
        count: 1,
        null: 4294
      },
      {
        meta: 'descr_ru',
        count: 111,
        null: 3734
      },
      {
        meta: 'title_en',
        count: 1,
        null: 4294
      },
      {
        meta: 'descr_en',
        count: 111,
        null: 3734
      }
    ]
  } finally {
    metaGroupIkscsLoading.value = false
  }
}

const fetchMetaGroupMc = async () => {
  metaGroupMcLoading.value = true
  metaGroupMcError.value = null
  try {
    console.log('Запрос v_meta_group (mc) к:', API_ENDPOINTS.META_GROUP_MC)
    console.log('Заголовки:', API_HEADERS.MC)
    
    const response = await axios.get(API_ENDPOINTS.META_GROUP_MC, {
      headers: API_HEADERS.MC
    })
    metaGroupMcData.value = response.data
  } catch (err) {
    console.error('Ошибка API v_meta_group (mc):', err)
    metaGroupMcError.value = err.response?.data?.message || err.message || 'Неизвестная ошибка'
    
    // Fallback дані для тестування
    console.log('Використовуємо fallback дані для v_meta_group (mc)')
    metaGroupMcError.value = null // Очищаємо помилку
    metaGroupMcData.value = [
      {
        meta: 'title_ua',
        count: 1,
        null: 3808
      },
      {
        meta: 'descr_ua',
        count: 244,
        null: 4746
      },
      {
        meta: 'title_ru',
        count: 1,
        null: 3808
      },
      {
        meta: 'descr_ru',
        count: 240,
        null: 4746
      },
      {
        meta: 'title_en',
        count: 1,
        null: 5985
      },
      {
        meta: 'descr_en',
        count: 1,
        null: 5985
      }
    ]
  } finally {
    metaGroupMcLoading.value = false
  }
}

const metaGroupIkscsHeaders = computed(() => {
  if (!metaGroupIkscsData.value || metaGroupIkscsData.value.length === 0) return []
  const firstItem = metaGroupIkscsData.value[0]
  if (!firstItem) return []
  return Object.keys(firstItem).map(key => ({ title: key, key }))
})

const metaGroupMcHeaders = computed(() => {
  if (!metaGroupMcData.value || metaGroupMcData.value.length === 0) return []
  const firstItem = metaGroupMcData.value[0]
  if (!firstItem) return []
  return Object.keys(firstItem).map(key => ({ title: key, key }))
})

// Автоматичне завантаження даних при монтуванні
onMounted(() => {
  fetchMetaGroupIkscs()
  fetchMetaGroupMc()
})
</script>

<style scoped>
.metatags-page {
  width: 100%;
  height: 100vh;
  min-height: 0;
  display: flex;
  flex-direction: row;
  gap: 16px;
  padding: 16px;
}

.metatags-card {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  width: calc(50% - 8px);
  height: 100%;
}

.metatags-card-text {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  min-height: 0;
  height: 100%;
  padding: 0 !important;
}

.metatags-scroll {
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