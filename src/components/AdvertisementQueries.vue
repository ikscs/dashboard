<template>
  <div class="advertisement-queries-page">
    <v-card class="welcome-card">
      <v-card-title class="d-flex align-center">
        <v-icon size="large" class="mr-3">mdi-database-plus</v-icon>
        Запись данных в таблицу _gads_select_query (схема ads)
      </v-card-title>
      
             <v-card-text>
                                                                               <div class="d-flex align-center mb-6">
                       <v-btn 
              color="primary" 
              size="large"
              @click="saveData"
              :loading="loading"
              :disabled="loading || !queryText.trim()"
              class="mr-4 align-center"
              style="height: 56px;"
            >
             <v-icon class="mr-2">mdi-play</v-icon>
             Запуск
           </v-btn>
           
                       <v-text-field
              v-model="targetField"
              label="Куда"
              placeholder="Автоматически заполняется словом после 'from'"
              variant="outlined"
              density="compact"
              :disabled="loading"
              class="target-field align-center"
              style="max-width: 300px; height: 56px;"
            ></v-text-field>
            
                         <v-btn
               color="secondary"
               variant="outlined"
               @click="openDocumentation"
               :disabled="loading"
               class="ml-4 align-center"
               style="height: 56px;"
             >
               <v-icon class="mr-2">mdi-book-open-variant</v-icon>
               Документация
             </v-btn>
             
             <v-checkbox
               v-model="addNewRecord"
               label="Добавить новую запись"
               :disabled="loading"
               class="ml-4 align-center"
               hide-details
               density="compact"
             ></v-checkbox>
         </div>
        
        <div v-if="loading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <div class="mt-4 text-body-1">Запись данных...</div>
        </div>
        
        <div v-else-if="error" class="text-center py-8">
          <v-alert type="error" variant="tonal">
            <v-alert-title>Ошибка записи данных</v-alert-title>
            {{ error }}
          </v-alert>
        </div>
        
        <div v-else-if="success" class="text-center py-8">
                     <v-alert type="success" variant="tonal">
             <v-alert-title>Данные успешно записаны</v-alert-title>
             {{ addNewRecord ? 'Запрос добавлен' : 'Запрос обновлен' }}: "{{ queryText }}"<br>
             <strong>Таблица:</strong> {{ targetField }}
           </v-alert>
        </div>
        
        <div class="query-input-section">
          <v-label class="text-body-1 font-weight-medium mb-2">
            Введите текст запроса:
          </v-label>
                     <div class="resizable-textarea-container">
             <v-textarea
               v-model="queryText"
               placeholder="Введите текст запроса для записи в поле 'query' таблицы _gads_select_query..."
               variant="outlined"
               rows="8"
               auto-grow
               clearable
               :disabled="loading"
               class="query-textarea resizable-textarea"
               style="resize: both; overflow: auto;"
             ></v-textarea>
           </div>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS, API_HEADERS } from '../config/api'

// Данные для формы
const queryText = ref('')
const targetField = ref('')
const addNewRecord = ref(true) // По умолчанию включено
const loading = ref(false)
const error = ref(null)
const success = ref(false)

// Функция для извлечения слова после "from"
const extractWordAfterFrom = (text) => {
  if (!text || typeof text !== 'string') return ''
  
  const fromMatch = text.match(/\bfrom\s+(\w+)/i)
  if (fromMatch && fromMatch[1]) {
    return fromMatch[1]
  }
  return ''
}

// Следим за изменениями в queryText и обновляем targetField
const updateTargetField = () => {
  // Обновляем поле только если оно пустое
  if (!targetField.value.trim()) {
    targetField.value = extractWordAfterFrom(queryText.value)
  }
}

// Отслеживаем изменения в queryText
watch(queryText, updateTargetField, { immediate: true })

// Функция для открытия документации
const openDocumentation = () => {
  window.open('https://developers.google.com/google-ads/api/fields/v21/overview', '_blank')
}

// Запись данных в таблицу
const saveData = async () => {
  if (!queryText.value.trim()) {
    error.value = 'Пожалуйста, введите текст запроса'
    return
  }
  
  loading.value = true
  error.value = null
  success.value = false
  
  try {
    let response
    
    if (addNewRecord.value) {
      // Добавляем новую запись
      response = await axios.post(API_ENDPOINTS.GADS_SELECT_QUERY, {
        query: queryText.value.trim(),
        table_name: targetField.value.trim()
      }, {
        headers: API_HEADERS.ADV
      })
    } else {
      // Получаем последний ID для редактирования
      const getResponse = await axios.get(API_ENDPOINTS.GADS_SELECT_QUERY, {
        headers: API_HEADERS.ADV
      })
      
      if (getResponse.data && getResponse.data.length > 0) {
        // Находим максимальный ID
        const maxId = Math.max(...getResponse.data.map(item => item.id || 0))
        
        // Редактируем запись с максимальным ID
        response = await axios.put(`${API_ENDPOINTS.GADS_SELECT_QUERY}?id=eq.${maxId}`, {
          query: queryText.value.trim(),
          table_name: targetField.value.trim()
        }, {
          headers: API_HEADERS.ADV
        })
      } else {
        error.value = 'Нет записей для редактирования'
        return
      }
    }
    
    console.log('GADS Queries Save Response:', response)
    console.log('GADS Queries Save Response data:', response.data)
    
    success.value = true
    // Очищаем поля после успешной записи
    queryText.value = ''
    targetField.value = ''
    
  } catch (err) {
    console.error('GADS Queries Save Error:', err)
    error.value = err.response?.data?.message || err.message || 'Ошибка записи данных'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.advertisement-queries-page {
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

 .query-input-section {
   margin-top: 16px;
 }
 
 .target-field {
   flex-shrink: 0;
 }
 
 /* Выравнивание всех элементов по центру */
 .d-flex.align-center > * {
   align-self: center;
 }

 .query-textarea {
   font-family: 'Courier New', monospace;
   font-size: 14px;
 }
 
 .resizable-textarea-container {
   position: relative;
   display: inline-block;
   width: 100%;
 }
 
 .resizable-textarea {
   min-width: 100%;
   min-height: 200px;
   max-height: 600px;
 }

 /* Стили для textarea */
 :deep(.v-textarea .v-field__input) {
   min-height: 200px;
   padding: 16px;
   resize: both;
   overflow: auto;
 }
 
 :deep(.v-textarea .v-field) {
   resize: both;
   overflow: auto;
   min-height: 200px;
   max-height: 600px;
 }

:deep(.v-textarea .v-field__outline) {
  border-radius: 8px;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .advertisement-queries-page {
    padding: 10px;
  }
  
  :deep(.v-textarea .v-field__input) {
    min-height: 150px;
    padding: 12px;
  }
}
</style>
