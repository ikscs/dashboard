<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS, API_HEADERS, API_BASE_URL, getDocsUrl } from './config/api'
import { useRouter } from 'vue-router'
import DashboardIcon from './components/icons/DashboardIcon.vue'

const router = useRouter()
const drawer = ref(true)
const rail = ref(true)
const theme = ref('light')
const settingsGroupOpen = ref(false)
const seoGroupOpen = ref(false)
const advertisementGroupOpen = ref(false)
const message = ref('Загрузка...')
const error = ref(null)
const loading = ref(false)

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

const toggleDrawer = () => {
  rail.value = !rail.value
  // Якщо згортаємо сайтбар, закриваємо підменю
  if (rail.value) {
    settingsGroupOpen.value = false
    seoGroupOpen.value = false
  }
}

const handleGroupClick = (groupName) => {
  // Якщо сайтбар згорнутий, розгортаємо його для показу підменю
  if (rail.value) {
    console.log('Розгортаємо сайтбар для показу підменю')
    rail.value = false
    
    if (groupName === 'settings') {
      settingsGroupOpen.value = true
    } else if (groupName === 'seo') {
      seoGroupOpen.value = true
    } else if (groupName === 'advertisement') {
      advertisementGroupOpen.value = true
    }
    
    // Затримка для відкриття підменю після розгортання сайтбара
    setTimeout(() => {
      // Знаходимо елемент v-list-group і відкриваємо його
      const groupElement = document.querySelector(`.v-list-group[value="${groupName}"]`)
      if (groupElement) {
        const activator = groupElement.querySelector('.v-list-group__header')
        if (activator) {
          activator.click()
        }
      }
    }, 100) // Невелика затримка для завершення анімації розгортання
  }
}

const navigateTo = (path) => {
  router.push(path)
}

const openHelp = async () => {
  const currentPath = router.currentRoute.value.path
  console.log('Текущий путь:', currentPath)
  
  // Если мы находимся на странице Help, открываем общую документацию
  if (currentPath === '/help') {
    window.open(getDocsUrl('general'), '_blank')
    return
  }
  
  try {
    console.log('Починаємо пошук URL документації для:', currentPath)
    const helpUrl = await getHelpUrlForPath(currentPath)
    console.log('Знайдений URL документації:', helpUrl)
    
    if (helpUrl) {
      try {
        console.log('Спроба відкрити документацію:', helpUrl)
        const newWindow = window.open(helpUrl, '_blank')
        if (!newWindow) {
          // Если popup заблокирован, показываем сообщение
          console.warn('Браузер заблокував відкриття вікна')
          alert('Браузер заблокував відкриття вікна. Дозвольте спливаючі вікна для цього сайту.')
        } else {
          console.log('Документація успішно відкрита')
        }
      } catch (error) {
        console.error('Помилка при відкритті документації:', error)
        alert('Помилка при відкритті документації. Спробуйте ще раз.')
      }
    } else {
      // Если нет специфичной документации, открываем общую
      console.log('Специфічна документація не знайдена, відкриваємо загальну')
      window.open(getDocsUrl('general'), '_blank')
    }
  } catch (error) {
    console.error('Критична помилка при отриманні URL документації:', error)
    console.error('Деталі помилки:', {
      message: error.message,
      stack: error.stack,
      currentPath: currentPath
    })
    
    // Если произошла ошибка, открываем общую документацию
    try {
      window.open(getDocsUrl('general'), '_blank')
    } catch (fallbackError) {
      console.error('Навіть fallback не працює:', fallbackError)
      alert('Помилка при відкритті документації. Перевірте консоль браузера для деталей.')
    }
  }
}

// Альтернативная функция для перехода к Help с параметром
const goToHelp = () => {
  const currentPath = router.currentRoute.value.path
  const section = getSectionFromPath(currentPath)
  if (section) {
    router.push({ path: '/help', query: { section } })
  } else {
    router.push('/help')
  }
}

const getSectionFromPath = (path) => {
  const pathMap = {
    '/': 'dashboard',
    '/finance': 'finance',
    '/advertisement': 'advertisement',
    '/seo': 'top',
    '/seo/top': 'top',
    '/seo/metatags': 'metatags',
    '/market': 'market',
    '/cp': 'cp',
    '/projects': 'projects',
    '/settings': 'settings',
    '/currency-rates': 'currency-rates'
  }
  return pathMap[path] || null
}

const getHelpUrlForPath = async (path) => {
  console.log('getHelpUrlForPath викликана з path:', path)
  
  // Мапінг шляхів до секцій
  const pathToSection = {
    '/': 'dashboard',
    '/finance': 'finance',
    '/advertisement': 'advertisement',
    '/advertisement/queries': 'advertisement',
    '/seo': 'seo',
    '/seo/top': 'seo-top',
    '/seo/metatags': 'seo-metatags',
    '/seo/metatags-check': 'seo-metatags-gen',
    '/market': 'market',
    '/cp': 'cp',
    '/projects': 'projects',
    '/settings': 'settings',
    '/currency-rates': 'currency-rates'
  }
  
  const section = pathToSection[path]
  console.log('Знайдена секція для path:', section)
  
  if (!section) {
    console.log('Секція не знайдена для path:', path)
    return null
  }
  
  // Fallback до старих посилань, якщо база недоступна
  const fallbackMap = {
    '/': getDocsUrl('dashboard'),
    '/finance': getDocsUrl('finance'),
    '/advertisement': getDocsUrl('advertisement'),
    '/seo': getDocsUrl('seo'),
    '/seo/top': getDocsUrl('seo/top'),
    '/seo/metatags': getDocsUrl('seo/metatags'),
    '/seo/metatags-check': getDocsUrl('seo/metatags-gen'),
    '/market': getDocsUrl('market'),
    '/cp': getDocsUrl('cp'),
    '/projects': getDocsUrl('projects'),
    '/settings': getDocsUrl('settings'),
    '/currency-rates': getDocsUrl('currency-rates')
  }
  
  // Завантажуємо посилання з бази даних
  try {
    console.log('Спроба завантажити посилання з API:', API_ENDPOINTS.HELP)
    
    const response = await axios.get(API_ENDPOINTS.HELP, {
      timeout: 5000, // Таймаут 5 секунд
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    })
    
    if (response.data && response.data.length > 0) {
      const links = response.data
      console.log('Посилання з бази даних:', links)
      
      const link = links.find(item => item.component === section)
      console.log('Знайдене посилання для секції', section, ':', link)
      
      if (link && link.url) {
        console.log('Повертаємо URL з бази даних:', link.url)
        return link.url
      }
    }
  } catch (error) {
    console.error('Помилка при завантаженні посилань з бази даних:', error)
    console.error('Деталі помилки:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data
    })
  }
  
  // Якщо база недоступна, використовуємо fallback
  const fallbackUrl = fallbackMap[path]
  console.log('Використовуємо fallback URL:', fallbackUrl)
  return fallbackUrl || null
}

const getPageTitle = () => {
  const currentPath = router.currentRoute.value.path
  const titleMap = {
    '/': 'DashBoard',
    '/finance': 'Финансы',
    '/advertisement': 'Реклама',
    '/seo': 'SEO',
    '/seo/top': 'SEO - Top',
    '/seo/metatags': 'SEO - MetaTegs',
    '/seo/metatags-check': 'SEO - MetaTegs GEN - Дерево категорій',
    '/market': 'Market',
    '/cp': 'CP',
    '/projects': 'Проекты',
    '/settings': 'Настройки',
    '/help': 'Помощь',
    '/currency-rates': 'Курсы валют'
  }
  return titleMap[currentPath] || 'DashBoard'
}

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

onMounted(() => {
  fetchMessage()
})
</script>

<template>
  <v-app :theme="theme">
    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      location="left"
      class="nav-drawer"
    >
      <v-list>
        <v-list-item
          prepend-icon="mdi-menu"
          @click="toggleDrawer"
        ></v-list-item>

        <v-divider></v-divider>

        <v-list-item
          :prepend-icon="DashboardIcon"
          title="DashBoard"
          :active="router.currentRoute.value.path === '/'"
          @click="navigateTo('/')"
        ></v-list-item>
        
        <v-list-item
          prepend-icon="mdi-cash-multiple"
          title="Финансы"
          :active="router.currentRoute.value.path === '/finance'"
          @click="navigateTo('/finance')"
        ></v-list-item>

        <v-list-group 
          value="advertisement" 
          :model-value="advertisementGroupOpen || !rail"
          @update:model-value="advertisementGroupOpen = $event"
        >
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-google-ads"
              title="Реклама"
              :active="router.currentRoute.value.path.startsWith('/advertisement')"
              @click.stop="handleGroupClick('advertisement')"
              @mousedown="rail && handleGroupClick('advertisement')"
            >
              <template v-slot:append v-if="rail">
                <v-icon size="small" class="ml-1">mdi-chevron-right</v-icon>
              </template>
            </v-list-item>
          </template>

          <v-list-item
            prepend-icon="mdi-google-ads"
            title="Основные данные"
            :active="router.currentRoute.value.path === '/advertisement'"
            @click="navigateTo('/advertisement')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-database-search"
            title="Запросы"
            :active="router.currentRoute.value.path === '/advertisement/queries'"
            @click="navigateTo('/advertisement/queries')"
          ></v-list-item>
        </v-list-group>

        <v-list-group 
          value="seo" 
          :model-value="seoGroupOpen || !rail"
          @update:model-value="seoGroupOpen = $event"
        >
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-magnify"
              title="SEO"
              @click.stop="handleGroupClick('seo')"
              @mousedown="rail && handleGroupClick('seo')"
            >
              <template v-slot:append v-if="rail">
                <v-icon size="small" class="ml-1">mdi-chevron-right</v-icon>
              </template>
            </v-list-item>
          </template>



          <v-list-item
            prepend-icon="mdi-table"
            title="Top (таблиця)"
            @click="navigateTo('/seo/top')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-tag-multiple"
            title="MetaTegs"
            @click="navigateTo('/seo/metatags')"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-tag-multiple-check"
            title="MetaTegs GEN"
            @click="navigateTo('/seo/metatags-check')"
          ></v-list-item>
        </v-list-group>

        <v-list-item
          prepend-icon="mdi-store"
          title="Market"
          @click="navigateTo('/market')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-account-group"
          title="CP"
          @click="navigateTo('/cp')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-folder-multiple"
          title="Проекти"
          @click="navigateTo('/projects')"
        ></v-list-item>

        <v-list-group 
          value="settings" 
          :model-value="settingsGroupOpen || !rail"
          @update:model-value="settingsGroupOpen = $event"
        >
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              prepend-icon="mdi-cog"
              title="Налаштування"
              @click.stop="handleGroupClick('settings')"
              @mousedown="rail && handleGroupClick('settings')"
            >
              <template v-slot:append v-if="rail">
                <v-icon size="small" class="ml-1">mdi-chevron-right</v-icon>
              </template>
            </v-list-item>
          </template>

          <v-list-item
            prepend-icon="mdi-help-circle"
            title="Help"
            @click="openHelp"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-cog"
            title="Редагувати Help"
            @click="navigateTo('/help')"
          ></v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      :elevation="1"
      class="app-bar"
    >
      <v-toolbar-title>{{ getPageTitle() }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        :icon="theme === 'light' ? 'mdi-weather-night' : 'mdi-weather-sunny'"
        @click="toggleTheme"
      ></v-btn>
      <v-btn
        icon="mdi-help-circle"
        @click="openHelp"
        class="ml-2"
        title="Відкрити документацію"
      ></v-btn>
    </v-app-bar>

    <div class="main-wrapper">
      <v-main class="main-content">
        <div class="content-wrapper">
          <router-view></router-view>
        </div>
      </v-main>
    </div>
  </v-app>
</template>

<style>
:root {
  --v-layout-left: 256px;
  --v-layout-top: 64px;
}

.v-application {
  background: #f5f5f5 !important;
  width: 100vw !important;
  min-width: 100vw !important;
  max-width: 100vw !important;
  overflow-x: hidden !important;
}

.v-application--wrap {
  width: 100vw !important;
  min-width: 100vw !important;
  max-width: 100vw !important;
  overflow-x: hidden !important;
}

.nav-drawer {
  background-color: rgb(var(--v-theme-surface)) !important;
  position: fixed !important;
  left: 0 !important;
  top: 0 !important;
  height: 100vh !important;
  z-index: 1000 !important;
  width: var(--v-layout-left) !important;
  transition: width 0.3s ease-in-out !important;
}

.v-list-item {
  border-radius: 8px;
  margin: 4px 8px;
}

.v-list-item:hover {
  background-color: rgb(var(--v-theme-surface-variant));
}

.v-list-item--active {
  background-color: rgb(var(--v-theme-primary)) !important;
  color: rgb(var(--v-theme-on-primary)) !important;
}

.app-bar {
  background-color: rgb(var(--v-theme-surface)) !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  position: fixed !important;
  left: var(--v-layout-left) !important;
  right: 0 !important;
  top: 0 !important;
  z-index: 999 !important;
  transition: left 0.3s ease-in-out !important;
}

.main-wrapper {
  position: fixed !important;
  left: var(--v-layout-left) !important;
  top: var(--v-layout-top) !important;
  width: calc(100% - var(--v-layout-left)) !important;
  height: calc(100vh - var(--v-layout-top)) !important;
  transition: left 0.3s ease-in-out !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  background-image: url('@/assets/bg_finance_light.png');
  background-size: auto;
  background-position: center;
  background-repeat: repeat;
}

.v-theme--dark .main-wrapper {
  background-image: url('@/assets/bg_finance_dark.png');
}

.main-content {
  width: 100% !important;
  height: 100% !important;
  position: relative !important;
  padding: 0 !important;
  margin: 0 !important;
  flex: 1 1 auto !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
}

.content-wrapper {
  padding: 24px !important;
  height: 100% !important;
  width: 100% !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
}

/* Стили для свернутого меню */
.nav-drawer.v-navigation-drawer--rail {
  width: 64px !important;
}

.nav-drawer.v-navigation-drawer--rail + .app-bar {
  left: 64px !important;
}

.nav-drawer.v-navigation-drawer--rail ~ .main-wrapper {
  left: 64px !important;
  width: calc(100% - 64px) !important;
}

/* Переопределение стилей Vuetify */
.v-layout {
  width: 100vw !important;
  min-width: 100vw !important;
  max-width: 100vw !important;
  overflow-x: hidden !important;
}

.v-layout--full-height {
  width: 100vw !important;
  min-width: 100vw !important;
  max-width: 100vw !important;
  overflow-x: hidden !important;
}

.v-main {
  flex: 1 1 auto !important;
  max-width: none !important;
  width: 100% !important;
  position: relative !important;
  transition: margin-left 0.3s ease-in-out !important;
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
}

.v-main__wrap {
  display: flex !important;
  flex: 1 1 auto !important;
  max-width: none !important;
  width: 100% !important;
  position: relative !important;
  padding: 0 !important;
  margin: 0 !important;
  flex-direction: column !important;
  align-items: flex-start !important;
}

.v-container.v-container--fluid {
  background-image: none !important;
  background: none !important;
}

[data-v-9b21acc4] {
  background-image: none !important;
  background: none !important;
}
</style>
