<template>
  <div class="help-page">
    <v-card class="welcome-card">
      <v-card-title class="d-flex align-center">
        <v-icon size="large" class="mr-3">mdi-help-circle</v-icon>
        Управление ссылками на документацию
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
        
        <!-- Кнопка инициализации базы данных -->
        <div class="mb-6">
          <v-btn
            color="secondary"
            variant="outlined"
            @click="showInitializer = true"
            prepend-icon="mdi-database-plus"
            class="mb-4"
          >
            Инициализировать базу данных
          </v-btn>
        </div>
        
        <!-- Форма для добавления/редактирования -->
        <v-form @submit.prevent="saveHelpLink" class="mb-6">
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.component"
                label="Компонент (идентификатор меню)"
                placeholder="Например: dashboard, finance, advertisement"
                variant="outlined"
                :disabled="loading"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.url"
                label="URL документации"
                placeholder="https://dashboard.api4/docs/..."
                variant="outlined"
                :disabled="loading"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="2">
              <v-btn
                type="submit"
                color="primary"
                :loading="loading"
                :disabled="!formData.component.trim() || !formData.url.trim()"
                block
              >
                {{ editingId ? 'Обновить' : 'Добавить' }}
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
        
        <!-- Таблица существующих ссылок -->
        <v-data-table
          :headers="headers"
          :items="helpLinks"
          :loading="loading"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn
              size="small"
              color="primary"
              variant="text"
              @click="editLink(item)"
              class="mr-2"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              size="small"
              color="error"
              variant="text"
              @click="deleteLink(item.id)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
          
          <template v-slot:item.url="{ item }">
            <a :href="item.url" target="_blank" class="text-decoration-none">
              {{ item.url }}
            </a>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
    
    <!-- Диалог инициализации -->
    <v-dialog v-model="showInitializer" max-width="800px">
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon size="large" class="mr-3">mdi-database-plus</v-icon>
          Инициализация базы данных Help
        </v-card-title>
        <v-card-text>
          <HelpInitializer />
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="showInitializer = false"
          >
            Закрыть
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'
import HelpInitializer from './HelpInitializer.vue'

const helpLinks = ref([])
const loading = ref(false)
const error = ref(null)
const success = ref(null)
const editingId = ref(null)
const showInitializer = ref(false)

const formData = ref({
  component: '',
  url: ''
})

const headers = [
  { title: 'ID', key: 'id', sortable: true },
  { title: 'Компонент', key: 'component', sortable: true },
  { title: 'URL', key: 'url', sortable: false },
  { title: 'Действия', key: 'actions', sortable: false, width: '120px' }
]

const loadHelpLinks = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(API_ENDPOINTS.HELP)
    helpLinks.value = response.data || []
    
    // Если есть данные, закрываем диалог инициализации
    if (response.data && response.data.length > 0) {
      showInitializer.value = false
    }
  } catch (err) {
    error.value = 'Ошибка при загрузке ссылок: ' + (err.response?.data?.message || err.message)
  } finally {
    loading.value = false
  }
}

const saveHelpLink = async () => {
  if (!formData.value.component.trim() || !formData.value.url.trim()) {
    error.value = 'Пожалуйста, заполните все поля'
    return
  }
  
  loading.value = true
  error.value = null
  success.value = null
  
  try {
    if (editingId.value) {
      // Обновление существующей записи
      await axios.patch(`${API_ENDPOINTS.HELP}?id=eq.${editingId.value}`, {
        component: formData.value.component.trim(),
        url: formData.value.url.trim()
      })
      success.value = 'Ссылка успешно обновлена'
    } else {
      // Добавление новой записи
      await axios.post(API_ENDPOINTS.HELP, {
        component: formData.value.component.trim(),
        url: formData.value.url.trim()
      })
      success.value = 'Ссылка успешно добавлена'
    }
    
    // Очистка формы
    formData.value = { component: '', url: '' }
    editingId.value = null
    
    // Перезагрузка данных
    await loadHelpLinks()
    
    // Очистка сообщения об успехе через 3 секунды
    setTimeout(() => {
      success.value = null
    }, 3000)
    
  } catch (err) {
    error.value = 'Ошибка при сохранении: ' + (err.response?.data?.message || err.message)
  } finally {
    loading.value = false
  }
}

const editLink = (item) => {
  formData.value = {
    component: item.component,
    url: item.url
  }
  editingId.value = item.id
}

const deleteLink = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить эту ссылку?')) {
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    await axios.delete(`${API_ENDPOINTS.HELP}?id=eq.${id}`)
    success.value = 'Ссылка успешно удалена'
    await loadHelpLinks()
    
    setTimeout(() => {
      success.value = null
    }, 3000)
    
  } catch (err) {
    error.value = 'Ошибка при удалении: ' + (err.response?.data?.message || err.message)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadHelpLinks()
})
</script>

<style scoped>
.help-page {
  padding: 20px;
}

.welcome-card {
  max-width: 1200px;
  margin: 0 auto;
}
</style> 