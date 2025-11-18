<template>
  <div class="metategs-check-page">
    <v-card class="welcome-card">
      <v-card-title class="d-flex align-center">
        <v-icon size="large" class="mr-3">mdi-tag-multiple</v-icon>
                 MetaTegs GEN - Дерево категорій
      </v-card-title>
      
      <v-card-text>
        <div class="domain-selection-section">
          <v-label class="text-body-1 font-weight-medium mb-2">
            Виберіть домен для перевірки:
          </v-label>
          
          <v-select
            v-model="selectedDomain"
            :items="availableDomains"
            label="Домен"
            variant="outlined"
            placeholder="Оберіть домен зі списку"
            class="mb-4"
            style="max-width: 400px;"
          >
            <template v-slot:item="{ item, props }">
              <v-list-item v-bind="props">
                <template v-slot:prepend>
                  <v-icon>mdi-web</v-icon>
                </template>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.value }}</v-list-item-subtitle>
              </v-list-item>
            </template>
          </v-select>
          
                     <v-btn
             v-if="selectedDomain"
             color="secondary"
             variant="outlined"
             size="small"
             @click="loadCategories"
             :loading="categoriesLoading"
             class="ml-4"
             prepend-icon="mdi-refresh"
           >
             Завантажити категорії
           </v-btn>
           
           <v-btn
             v-if="selectedDomain"
             color="info"
             variant="outlined"
             size="small"
             @click="loadTestData"
             class="ml-2"
             prepend-icon="mdi-database"
           >
             Тестові дані
           </v-btn>
           
                       <v-btn
              v-if="selectedDomain"
              color="warning"
              variant="outlined"
              size="small"
              @click="testAPIOnly"
              class="ml-2"
              prepend-icon="mdi-api"
            >
              Тест API
            </v-btn>
            
            <v-btn
              v-if="selectedDomain && selectedDomain.title === 'IKSCS'"
              color="error"
              variant="outlined"
              size="small"
              @click="testIKSCSWithCP"
              class="ml-2"
              prepend-icon="mdi-database-search"
            >
              Тест CP заголовок
            </v-btn>
            
            <v-btn
              v-if="selectedDomain && selectedDomain.title === 'IKSCS'"
              color="success"
              variant="outlined"
              size="small"
              @click="testIKSCSOriginal"
              class="ml-2"
              prepend-icon="mdi-database"
            >
              Тест IKSCS заголовок
            </v-btn>
        </div>
        
                 <!-- Таблиця категорій -->
         <div v-if="selectedDomain" class="categories-section mt-6">
           <v-divider class="mb-4"></v-divider>
           
           <div class="d-flex align-center mb-4">
             <v-icon class="mr-2">mdi-table</v-icon>
             <h3 class="text-h6 mb-0">Категорії товарів</h3>
             
             <v-chip
               size="small"
               variant="outlined"
               class="ml-4"
               :color="categoriesData.length > 0 ? 'success' : 'warning'"
             >
               {{ categoriesData.length }} категорій
             </v-chip>
             
             <v-chip
               v-if="categoriesError"
               size="small"
               variant="outlined"
               class="ml-2"
               color="error"
             >
               Помилка: {{ categoriesError }}
             </v-chip>
           </div>
           
           <div v-if="categoriesLoading" class="text-center py-8">
             <v-progress-circular indeterminate color="primary" size="32"></v-progress-circular>
             <div class="mt-2 text-body-2">Завантаження категорій...</div>
           </div>
           
           <div v-else-if="categoriesError" class="text-center py-4">
             <v-alert type="error" variant="tonal" class="mb-0">
               {{ categoriesError }}
             </v-alert>
           </div>
           
                       <div v-else-if="categoriesData.length > 0" class="categories-table">
              <!-- Фільтри та статистика -->
              <div class="d-flex align-center justify-space-between mb-4">
                                 <div class="d-flex align-center">
                   <v-chip
                     size="small"
                     variant="outlined"
                     color="info"
                     class="mr-2"
                   >
                     Всього: {{ categoriesData.length }}
                   </v-chip>
                   <v-chip
                     size="small"
                     variant="outlined"
                     color="success"
                     class="mr-2"
                   >
                     Опубліковано: {{ categoriesData.filter(c => c.category_publish).length }}
                   </v-chip>
                   <v-chip
                     size="small"
                     variant="outlined"
                     color="warning"
                     class="mr-2"
                   >
                     Приховано: {{ categoriesData.filter(c => !c.category_publish).length }}
                   </v-chip>
                   <v-chip
                     size="small"
                     variant="outlined"
                     color="primary"
                   >
                     Порядок: {{ Math.max(...categoriesData.map(c => c.ordering || 0)) }}
                   </v-chip>
                 </div>
                
                <v-select
                  v-model="sortBy"
                  :items="sortOptions"
                  label="Сортування"
                  variant="outlined"
                  density="compact"
                  style="max-width: 200px;"
                ></v-select>
              </div>
              
                             <v-table>
                 <thead>
                   <tr>
                     <th class="text-left">ID категорії</th>
                     <th class="text-left">Назва (UK)</th>
                     <th class="text-left">Батьківський ID</th>
                     <th class="text-left">Порядок</th>
                     <th class="text-left">Опубліковано</th>
                   </tr>
                 </thead>
                 <tbody>
                   <tr v-for="category in sortedCategories" :key="category.category_id">
                     <td>{{ category.category_id }}</td>
                     <td>{{ category['name_uk-UA'] || 'Назва відсутня' }}</td>
                     <td>
                       <span v-if="category.category_parent_id === 0">Коренева</span>
                       <span v-else>{{ category.category_parent_id }}</span>
                     </td>
                     <td>
                       <v-chip
                         size="small"
                         variant="outlined"
                         color="primary"
                       >
                         {{ category.ordering || 0 }}
                       </v-chip>
                     </td>
                     <td>
                       <v-chip
                         :color="category.category_publish ? 'success' : 'error'"
                         size="small"
                         variant="outlined"
                       >
                         {{ category.category_publish ? 'Так' : 'Ні' }}
                       </v-chip>
                     </td>
                   </tr>
                 </tbody>
               </v-table>
            </div>
           
           <div v-else class="text-center py-4">
             <v-alert type="info" variant="tonal">
               <v-alert-title>Категорії не знайдено</v-alert-title>
               <div class="mt-2">
                 <p>Спробуйте:</p>
                 <ul class="text-left">
                   <li>Натиснути кнопку "Тестові дані" для перевірки</li>
                   <li>Перевірити консоль браузера на помилки</li>
                   <li>Переконатися, що API доступний</li>
                 </ul>
               </div>
             </v-alert>
           </div>
         </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS, API_HEADERS } from '@/config/api.js'

const selectedDomain = ref(null)

const availableDomains = [
  {
    title: 'IKSCS',
    value: 'ikscs.in.ua'
  },
  {
    title: 'Mobile City',
    value: 'mobilecity.com.ua'
  }
]

// Дані для категорій
const categoriesData = ref([])
const categoriesLoading = ref(false)
const categoriesError = ref(null)

// Сортування
const sortBy = ref('id')
const sortOptions = [
  { title: 'За ID', value: 'id' },
  { title: 'За назвою', value: 'name' },
  { title: 'За батьківським ID', value: 'parent' },
  { title: 'За порядком', value: 'ordering' },
  { title: 'За статусом публікації', value: 'publish' }
]

// Відсортовані категорії
const sortedCategories = computed(() => {
  if (!categoriesData.value.length) return []
  
  const sorted = [...categoriesData.value]
  
  switch (sortBy.value) {
    case 'name':
      return sorted.sort((a, b) => (a['name_uk-UA'] || '').localeCompare(b['name_uk-UA'] || ''))
    case 'parent':
      return sorted.sort((a, b) => (a.category_parent_id || 0) - (b.category_parent_id || 0))
    case 'ordering':
      return sorted.sort((a, b) => (a.ordering || 0) - (b.ordering || 0))
    case 'publish':
      return sorted.sort((a, b) => Number(b.category_publish) - Number(a.category_publish))
    default: // 'id'
      return sorted.sort((a, b) => (a.category_id || 0) - (b.category_id || 0))
  }
})

// Функція для тестування IKSCS з CP схемою та IKSCS заголовком
const testIKSCSOriginal = async () => {
  if (selectedDomain.value?.title !== 'IKSCS') return
  
  console.log('🧪 ТЕСТУВАННЯ IKSCS З CP СХЕМОЮ ТА IKSCS ЗАГОЛОВКОМ')
  console.log('Домен:', selectedDomain.value.title)
  
  try {
    const endpoint = API_ENDPOINTS.CATEGORIES_IKSCS
    const headers = API_HEADERS.IKSCS
    
    console.log('Ендпоінт оригінал:', endpoint)
    console.log('Заголовки оригінал:', headers)
    console.log('Повний URL оригінал:', endpoint)
    
    const response = await axios.get(endpoint, { headers })
    console.log('✅ Оригінальний API успішно відповів:', response.status)
    console.log('Дані оригінал:', response.data)
    
    if (response.data && response.data.length > 0) {
      categoriesData.value = response.data
      categoriesError.value = null
      console.log('✅ Дані завантажено з оригінальної схеми')
    } else {
      categoriesData.value = []
      categoriesError.value = 'Оригінальний API повернув порожній масив'
    }
    
  } catch (err) {
    console.error('❌ Оригінальний API помилка:', err)
    categoriesData.value = []
    categoriesError.value = `Оригінальний API помилка: ${err.message}`
  }
}

// Функція для тестування IKSCS з CP схемою та CP заголовком
const testIKSCSWithCP = async () => {
  if (selectedDomain.value?.title !== 'IKSCS') return
  
  console.log('🧪 ТЕСТУВАННЯ IKSCS З CP СХЕМОЮ ТА CP ЗАГОЛОВКОМ')
  console.log('Домен:', selectedDomain.value.title)
  
  try {
    const endpoint = API_ENDPOINTS.CATEGORIES_IKSCS
    const headers = API_HEADERS.CP
    
    console.log('Ендпоінт CP:', endpoint)
    console.log('Заголовки CP:', headers)
    console.log('Повний URL CP:', endpoint)
    
    const response = await axios.get(endpoint, { headers })
    console.log('✅ CP API успішно відповів:', response.status)
    console.log('Дані CP:', response.data)
    
    if (response.data && response.data.length > 0) {
      categoriesData.value = response.data
      categoriesError.value = null
      console.log('✅ Дані завантажено з CP схеми')
    } else {
      categoriesData.value = []
      categoriesError.value = 'CP API повернув порожній масив'
    }
    
  } catch (err) {
    console.error('❌ CP API помилка:', err)
    categoriesData.value = []
    categoriesError.value = `CP API помилка: ${err.message}`
  }
}

// Функція для тестування API без fallback даних
const testAPIOnly = async () => {
  if (!selectedDomain.value) return
  
  console.log('🧪 ТЕСТУВАННЯ API БЕЗ FALLBACK ДАНИХ')
  console.log('Домен:', selectedDomain.value.title)
  
  try {
    const endpoint = selectedDomain.value.title === 'IKSCS' 
      ? API_ENDPOINTS.CATEGORIES_IKSCS 
      : API_ENDPOINTS.CATEGORIES_MC
    
    const headers = selectedDomain.value.title === 'IKSCS' 
      ? API_HEADERS.IKSCS 
      : API_HEADERS.MC
    
    console.log('Ендпоінт:', endpoint)
    console.log('Заголовки:', headers)
    
    const response = await axios.get(endpoint, { headers })
    console.log('✅ API успішно відповів:', response.status)
    console.log('Дані:', response.data)
    
    if (response.data && response.data.length > 0) {
      categoriesData.value = response.data
      categoriesError.value = null
    } else {
      categoriesData.value = []
      categoriesError.value = 'API повернув порожній масив'
    }
    
  } catch (err) {
    console.error('❌ API помилка:', err)
    categoriesData.value = []
    categoriesError.value = `API помилка: ${err.message}`
  }
}

// Функція для завантаження тестових даних
const loadTestData = () => {
  console.log('Завантаження тестових даних для:', selectedDomain.value.title)
  
  if (selectedDomain.value.title === 'IKSCS') {
    const testData = [
      { category_id: 1, 'name_uk-UA': 'Електроніка', category_parent_id: 0, ordering: 1, category_publish: true },
      { category_id: 2, 'name_uk-UA': 'Комп\'ютери', category_parent_id: 1, ordering: 1, category_publish: true },
      { category_id: 3, 'name_uk-UA': 'Ноутбуки', category_parent_id: 2, ordering: 1, category_publish: true },
      { category_id: 4, 'name_uk-UA': 'Планшети', category_parent_id: 2, ordering: 2, category_publish: false },
      { category_id: 5, 'name_uk-UA': 'Телефони', category_parent_id: 1, ordering: 2, category_publish: true },
      { category_id: 6, 'name_uk-UA': 'Смартфони', category_parent_id: 5, ordering: 1, category_publish: true },
      { category_id: 7, 'name_uk-UA': 'Одяг', category_parent_id: 0, ordering: 2, category_publish: true },
      { category_id: 8, 'name_uk-UA': 'Чоловічий одяг', category_parent_id: 7, ordering: 1, category_publish: true },
      { category_id: 9, 'name_uk-UA': 'Жіночий одяг', category_parent_id: 7, ordering: 2, category_publish: false }
    ]
    categoriesData.value = testData
    console.log('Тестові дані IKSCS завантажено:', categoriesData.value)
  } else {
    const testData = [
      { category_id: 1, 'name_uk-UA': 'Мобільні телефони', category_parent_id: 0, ordering: 1, category_publish: true },
      { category_id: 2, 'name_uk-UA': 'iPhone', category_parent_id: 1, ordering: 1, category_publish: true },
      { category_id: 3, 'name_uk-UA': 'Samsung', category_parent_id: 1, ordering: 2, category_publish: true },
      { category_id: 4, 'name_uk-UA': 'Аксесуари', category_parent_id: 0, ordering: 2, category_publish: true },
      { category_id: 5, 'name_uk-UA': 'Чохли', category_parent_id: 4, ordering: 1, category_publish: false },
      { category_id: 6, 'name_uk-UA': 'Зарядні пристрої', category_parent_id: 4, ordering: 2, category_publish: true }
    ]
    categoriesData.value = testData
    console.log('Тестові дані MC завантажено:', categoriesData.value)
  }
  
  categoriesError.value = null
}

// Функція для завантаження категорій
const loadCategories = async () => {
  if (!selectedDomain.value) return
  
  categoriesLoading.value = true
  categoriesError.value = null
  
  try {
    const endpoint = selectedDomain.value.title === 'IKSCS' 
      ? API_ENDPOINTS.CATEGORIES_IKSCS 
      : API_ENDPOINTS.CATEGORIES_MC
    
    const headers = selectedDomain.value.title === 'IKSCS' 
      ? API_HEADERS.IKSCS 
      : API_HEADERS.MC
    
         console.log('=== ДЕТАЛЬНЕ ЛОГУВАННЯ ===')
     console.log('Завантаження категорій для:', selectedDomain.value.title)
     console.log('Ендпоінт:', endpoint)
     console.log('Заголовки:', headers)
     console.log('Повний URL:', endpoint)
     console.log('API_HEADERS.IKSCS:', API_HEADERS.IKSCS)
     console.log('API_HEADERS.MC:', API_HEADERS.MC)
     console.log('API_HEADERS.IKSCS:', API_HEADERS.IKSCS)
     console.log('API_HEADERS.MC:', API_HEADERS.MC)
     console.log('API_HEADERS.CP:', API_HEADERS.CP)
     console.log('Повний URL:', endpoint)
     console.log('========================')
    
    const response = await axios.get(endpoint, { headers })
    const categories = response.data || []
    
    console.log('=== ВІДПОВІДЬ API ===')
    console.log('Статус:', response.status)
    console.log('Заголовки відповіді:', response.headers)
    console.log('Дані категорій:', categories)
    console.log('Кількість категорій:', categories.length)
    console.log('Тип даних:', typeof categories)
    console.log('========================')
    
    if (categories.length === 0) {
      console.warn('⚠️ API повернув порожній масив категорій')
      categoriesError.value = 'API повернув порожній масив категорій'
      return
    }
    
    // Просто зберігаємо дані як є
    categoriesData.value = categories
    console.log('Дані категорій завантажено:', categoriesData.value)
    
  } catch (err) {
    console.error('❌ Помилка завантаження категорій:', err)
    console.error('Деталі помилки:', {
      message: err.message,
      status: err.response?.status,
      statusText: err.response?.statusText,
      data: err.response?.data,
      headers: err.response?.headers
    })
    
    categoriesError.value = err.response?.data?.message || err.message || 'Помилка завантаження категорій'
    
    // Fallback дані для тестування
    if (selectedDomain.value.title === 'IKSCS') {
      categoriesData.value = [
        { category_id: 1, 'name_uk-UA': 'Електроніка', category_parent_id: 0, ordering: 1, category_publish: true },
        { category_id: 2, 'name_uk-UA': 'Комп\'ютери', category_parent_id: 1, ordering: 1, category_publish: true },
        { category_id: 3, 'name_uk-UA': 'Ноутбуки', category_parent_id: 2, ordering: 1, category_publish: true },
        { category_id: 4, 'name_uk-UA': 'Планшети', category_parent_id: 2, ordering: 2, category_publish: false },
        { category_id: 5, 'name_uk-UA': 'Телефони', category_parent_id: 1, ordering: 2, category_publish: true },
        { category_id: 6, 'name_uk-UA': 'Смартфони', category_parent_id: 5, ordering: 1, category_publish: true },
        { category_id: 7, 'name_uk-UA': 'Одяг', category_parent_id: 0, ordering: 2, category_publish: true },
        { category_id: 8, 'name_uk-UA': 'Чоловічий одяг', category_parent_id: 7, ordering: 1, category_publish: true },
        { category_id: 9, 'name_uk-UA': 'Жіночий одяг', category_parent_id: 7, ordering: 2, category_publish: false }
      ]
    } else {
      categoriesData.value = [
        { category_id: 1, 'name_uk-UA': 'Мобільні телефони', category_parent_id: 0, ordering: 1, category_publish: true },
        { category_id: 2, 'name_uk-UA': 'iPhone', category_parent_id: 1, ordering: 1, category_publish: true },
        { category_id: 3, 'name_uk-UA': 'Samsung', category_parent_id: 1, ordering: 2, category_publish: true },
        { category_id: 4, 'name_uk-UA': 'Аксесуари', category_parent_id: 0, ordering: 2, category_publish: true },
        { category_id: 5, 'name_uk-UA': 'Чохли', category_parent_id: 4, ordering: 1, category_publish: false },
        { category_id: 6, 'name_uk-UA': 'Зарядні пристрої', category_parent_id: 4, ordering: 2, category_publish: true }
      ]
    }
    categoriesError.value = null
  } finally {
    categoriesLoading.value = false
  }
}



// Спостерігаємо за зміною вибраного домену
watch(selectedDomain, (newDomain, oldDomain) => {
  console.log('Зміна домену:', { old: oldDomain, new: newDomain })
  
  if (newDomain) {
    console.log('Виклик loadCategories для домену:', newDomain.title)
    loadCategories()
  } else {
    console.log('Очищення категорій')
    categoriesData.value = []
  }
})
</script>

<style scoped>
.metategs-check-page {
  padding: 20px;
}

.welcome-card {
  max-width: 800px;
  margin: 0 auto;
}

.domain-selection-section {
  margin-bottom: 20px;
}

.categories-section {
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  padding-top: 20px;
}

.categories-table {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 8px;
  overflow: hidden;
}

.categories-table :deep(.v-table) {
  background: transparent;
}

.categories-table :deep(.v-table__wrapper) {
  max-height: 500px;
  overflow-y: auto;
}
</style>
