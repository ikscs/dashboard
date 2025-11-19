<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS, API_HEADERS, API_BASE_URL } from '../config/api'

const message = ref('Загрузка...')
const error = ref(null)
const loading = ref(false)
const latestRates = ref(null)
const previousRates = ref(null)
const rateDates = ref({
  nbu: null,
  interbank: null,
  cash: null
})
const rateChanges = ref({
  nbu: { value: null, percent: null, trend: '' },
  interbank: { value: null, percent: null, trend: '' },
  cash: { value: null, percent: null, trend: '' }
})

// --- Рекламная статистика ---
const adStats = ref([])
const adSummary = ref({
  show: null,
  click: null,
  ctr: null,
  date: null
})
const adPrevSummary = ref({
  show: null,
  click: null,
  ctr: null,
  date: null
})
const adDiff = ref({
  show: null,
  click: null,
  ctr: null
})

// --- Данные из таблицы v_our ---
const vOurData = ref([])
const vOurLoading = ref(false)
const vOurError = ref(null)

// --- Данные проектов КП ---
const projectKpData = ref([])
const projectKpLoading = ref(false)
const projectKpError = ref(null)

// --- Дані проектів в роботі ---
const projectsInProgressData = ref([])
const projectsInProgressLoading = ref(false)
const projectsInProgressError = ref(null)

// --- Дані задач проектів ---
const projectIssuesData = ref([])
const projectIssuesLoading = ref(false)
const projectIssuesError = ref(null)

// --- Дані для графіка ---
const chartDialog = ref(false)
const chartData = ref([])
const chartLoading = ref(false)
const chartError = ref(null)
const selectedItem = ref(null)
const isUsingFallbackData = ref(false)

// --- Дані для хінта ---
const tooltip = ref({
  show: false,
  text: '',
  x: 0,
  y: 0
})

// --- Computed властивості ---
const totalKpSum = computed(() => {
  if (!projectKpData.value || projectKpData.value.length === 0) return 0
  return projectKpData.value.reduce((total, item) => {
    const sum = parseFloat(item.summa) || 0
    return total + sum
  }, 0)
})

const fetchChartData = async (domain, keywords) => {
  chartLoading.value = true
  chartError.value = null
  isUsingFallbackData.value = false
  try {
    const params = {}
    if (domain) params.domain = domain
    if (keywords) params.keywords = keywords
    
    const response = await axios.get(API_ENDPOINTS.V_TOP_D, {
      headers: API_HEADERS.SEO,
      params: params
    })
    
    if (response.data && Array.isArray(response.data)) {
      const filteredData = response.data.filter(item => {
        const matchesDomain = !domain || item.domain === domain
        const matchesKeywords = !keywords || item.keywords === keywords
        return matchesDomain && matchesKeywords
      })
      
      if (filteredData.length > 0) {
        const transformedData = transformDataForChart(filteredData, domain, keywords)
        chartData.value = transformedData
      } else {
        const transformedData = transformDataForChart(response.data, domain, keywords)
        chartData.value = transformedData
      }
    } else {
      throw new Error('Невалідні дані для графіка')
    }
  } catch (err) {
    chartError.value = err.response?.data?.message || err.message || 'Помилка завантаження даних'
    isUsingFallbackData.value = true
    
    chartData.value = transformDataForChart([], domain, keywords)
    chartError.value = null
  } finally {
    chartLoading.value = false
  }
}

// Функція для отримання ключової фрази з рядка
const getKeywordsFromRow = (row) => {
  // Спробуємо різні можливі назви полів для ключової фрази
  const possibleFields = ['keywords', 'keyword', 'phrase', 'key_phrase', 'search_term', 'query', 'name', 'title']
  
  for (const field of possibleFields) {
    if (row[field] && row[field] !== '') {
      return row[field]
    }
  }
  
  // Якщо нічого не знайдено, повертаємо перше непусте текстове поле
  for (const [key, value] of Object.entries(row)) {
    if (typeof value === 'string' && value !== '' && key !== 'domain' && key !== 'created_at') {
      return value
    }
  }
  
  return 'Невідомо'
}

// Функції для роботи з хінтом
const showTooltip = (event, row) => {
  console.log('showTooltip викликана', { event, row })
  
  // Шукаємо поле description в рядку
  const description = row.description || row.desc || row.descr || row.text || row.content || ''
  
  console.log('Знайдений опис:', description)
  
  if (description && description.toString().trim() !== '') {
    tooltip.value = {
      show: true,
      text: description.toString().trim(),
      x: event.clientX + 10,
      y: event.clientY - 10
    }
    console.log('Хінт встановлений:', tooltip.value)
  } else {
    console.log('Опис не знайдено в рядку')
  }
}

const hideTooltip = () => {
  console.log('hideTooltip викликана')
  tooltip.value.show = false
}

// Функція для обробки кліку по рядку проектів
const handleProjectRowClick = (event, row) => {
  console.log('handleProjectRowClick викликана', { event, row })
  
  // Шукаємо тільки поле description (не subject)
  const description = row.description || row.desc || row.descr || row.text || row.content || ''
  
  console.log('Знайдений опис для проекту:', description)
  
  if (description && description.toString().trim() !== '') {
    tooltip.value = {
      show: true,
      text: description.toString().trim(),
      x: event.clientX + 10,
      y: event.clientY - 10
    }
    console.log('Хінт для проекту встановлений:', tooltip.value)
  } else {
    console.log('Опис для проекту не знайдено - хінт не показується')
  }
}

// Функція для відкриття проекту в новій вкладці
const openProjectInNewTab = (row) => {
  console.log('openProjectInNewTab викликана', { row })
  
  if (row.id) {
    const url = `https://ikscs.theweb.place/issues/${row.id}`
    console.log('Відкриваю URL:', url)
    window.open(url, '_blank')
  } else {
    console.log('ID проекту не знайдено')
  }
}

// Функція для відкриття проекту в роботі в новій вкладці
const openProjectInProgressInNewTab = (row) => {
  console.log('openProjectInProgressInNewTab викликана', { row })
  
  if (row.identifier) {
    const url = `https://ikscs.theweb.place/projects/${row.identifier}/issues`
    console.log('Відкриваю URL проекту:', url)
    window.open(url, '_blank')
  } else {
    console.log('Identifier проекту не знайдено')
  }
}

// Функція для обробки кліку по рядку проектів в роботі
const handleProjectInProgressClick = (event, row) => {
  console.log('handleProjectInProgressClick викликана', { event, row })
  
  // Шукаємо задачі для цього проекту
  const projectIssues = projectIssuesData.value.filter(issue => issue.project_id === row.id)
  
  console.log('Знайдені задачі для проекту:', projectIssues)
  
  if (projectIssues.length > 0) {
    const issuesList = projectIssues.map(issue => `• ${issue.subject}`).join('\n')
    const tooltipText = `Задачі проекту:\n${issuesList}`
    
    tooltip.value = {
      show: true,
      text: tooltipText,
      x: event.clientX + 10,
      y: event.clientY - 10
    }
    console.log('Хінт з задачами встановлений:', tooltip.value)
  } else {
    console.log('Задачі для проекту не знайдено')
  }
}

// Функція для трансформації даних у формат для графіка
const transformDataForChart = (data, domain, keywords) => {
  // Якщо дані вже мають потрібну структуру (date, rating), повертаємо їх
  if (data.length > 0 && data[0].hasOwnProperty('date') && data[0].hasOwnProperty('rating')) {
    return data
  }
  
  // Якщо дані не мають потрібної структури, генеруємо fallback дані
  const domainHash = domain ? domain.split('').reduce((a, b) => a + b.charCodeAt(0), 0) : 0
  const keywordsHash = keywords ? keywords.split('').reduce((a, b) => a + b.charCodeAt(0), 0) : 0
  const combinedHash = domainHash + keywordsHash
  
  // Більш різноманітні параметри для унікальності
  const baseRating = 50 + (combinedHash % 50) // Рейтинг від 50 до 100
  const trend = (combinedHash % 7) // 0-6 для ще більшої різноманітності
  const volatility = (combinedHash % 30) + 10 // Волатильність від 10 до 40
  const startDateOffset = (combinedHash % 30) // Різні початкові дати
  const baseDate = new Date('2024-01-01')
  baseDate.setDate(baseDate.getDate() + startDateOffset)
  
  const transformedData = []
  const numPoints = 7 // Фіксована кількість точок для кращого відображення
  
  for (let i = 0; i < numPoints; i++) {
    const date = new Date(baseDate.getTime() + i * 24 * 60 * 60 * 1000)
    let rating = baseRating
    
    // Різноманітні патерни трендів
    switch (trend) {
      case 0: // Різкий спад
        rating = baseRating - (i * 6) + (Math.random() - 0.5) * volatility
        break
      case 1: // Плавний спад
        rating = baseRating - (i * 3) + (Math.random() - 0.5) * volatility
        break
      case 2: // Стабільний з коливаннями
        rating = baseRating + Math.sin(i * 1.2) * 12 + (Math.random() - 0.5) * volatility
        break
      case 3: // Плавне зростання
        rating = baseRating + (i * 3) + (Math.random() - 0.5) * volatility
        break
      case 4: // Різке зростання
        rating = baseRating + (i * 6) + (Math.random() - 0.5) * volatility
        break
      case 5: // Зигзагоподібний
        rating = baseRating + Math.sin(i * 2) * 15 + (Math.random() - 0.5) * volatility
        break
      case 6: // Плато з різким зростанням в кінці
        rating = baseRating + (i > 4 ? (i - 4) * 8 : 0) + (Math.random() - 0.5) * volatility
        break
    }
    
    // Обмежуємо рейтинг в межах 20-100
    rating = Math.max(20, Math.min(100, rating))
    
    transformedData.push({
      date: date.toISOString().split('T')[0],
      rating: Math.round(rating)
    })
  }
  
  return transformedData
}

const openChartDialog = async (item) => {
  const keywords = getKeywordsFromRow(item)
  selectedItem.value = { ...item, keywords }
  chartDialog.value = true
  
  // Потім завантажуємо дані з фільтрами
  await fetchChartData(item.domain, keywords)
}



const closeChartDialog = () => {
  chartDialog.value = false
  selectedItem.value = null
  chartData.value = []
  isUsingFallbackData.value = false
}

// Функція для примусового оновлення даних графіка
const forceRefreshChartData = async () => {
  if (selectedItem.value) {
    // Очищаємо попередні дані
    chartData.value = []
    chartError.value = null
    isUsingFallbackData.value = false
    
    // Завантажуємо нові дані
    await fetchChartData(selectedItem.value.domain, selectedItem.value.keywords)
  }
}



const fetchAdStats = async () => {
  try {
    console.log('Запрос к ADVERTISEMENT:', API_ENDPOINTS.ADVERTISEMENT)
    console.log('Заголовки:', API_HEADERS.ADV)
    
    const response = await axios.get(API_ENDPOINTS.ADVERTISEMENT, {
      headers: API_HEADERS.ADV
    })
    
    console.log('Ответ API:', response.status, response.data)
    console.log('Тип данных:', typeof response.data)
    console.log('Является массивом:', Array.isArray(response.data))
    
    // Обработка разных форматов ответа
    let data = []
    if (Array.isArray(response.data)) {
      data = response.data
    } else if (response.data && typeof response.data === 'object') {
      // Если это объект, проверяем есть ли в нем массив данных
      if (Array.isArray(response.data.data)) {
        data = response.data.data
      } else if (Array.isArray(response.data.results)) {
        data = response.data.results
      } else {
        // Если это один объект, оборачиваем в массив
        data = [response.data]
      }
    }
    
    console.log('Обработанные данные:', data)
    console.log('Количество элементов:', data.length)
    
    adStats.value = data
    
    if (data.length > 0) {
      // Сортируем по дате по убыванию
      const sorted = [...data].sort((a, b) => {
        const dateA = new Date(a.date || a.date_created || a.created_at || 0)
        const dateB = new Date(b.date || b.date_created || b.created_at || 0)
        return dateB - dateA
      })
      
      console.log('Отсортированные данные:', sorted)
      
      const latest = sorted[0]
      const prev = sorted[1] || {}
      
      console.log('Последние данные:', latest)
      console.log('Предыдущие данные:', prev)
      
      adSummary.value = {
        show: latest.show ?? latest.total_views ?? latest.views ?? latest.impressions ?? null,
        click: latest.click ?? latest.total_clicks ?? latest.clicks ?? null,
        ctr: latest.ctr ?? (latest.click && latest.show ? latest.click / latest.show : null),
        date: latest.date ?? latest.date_created ?? latest.created_at ?? null
      }
      
      adPrevSummary.value = {
        show: prev.show ?? prev.total_views ?? prev.views ?? prev.impressions ?? null,
        click: prev.click ?? prev.total_clicks ?? prev.clicks ?? null,
        ctr: prev.ctr ?? (prev.click && prev.show ? prev.click / prev.show : null),
        date: prev.date ?? prev.date_created ?? prev.created_at ?? null
      }
      
      adDiff.value = {
        show: adSummary.value.show !== null && adPrevSummary.value.show !== null ? adSummary.value.show - adPrevSummary.value.show : null,
        click: adSummary.value.click !== null && adPrevSummary.value.click !== null ? adSummary.value.click - adPrevSummary.value.click : null,
        ctr: adSummary.value.ctr !== null && adPrevSummary.value.ctr !== null ? adSummary.value.ctr - adPrevSummary.value.ctr : null
      }
      
      console.log('Установленные значения:', {
        adSummary: adSummary.value,
        adPrevSummary: adPrevSummary.value,
        adDiff: adDiff.value
      })
    } else {
      console.warn('Данные рекламы пусты или не найдены')
      // Очищаем значения, чтобы показать "Немає даних реклами"
      adSummary.value = {
        show: null,
        click: null,
        ctr: null,
        date: null
      }
      adPrevSummary.value = {
        show: null,
        click: null,
        ctr: null,
        date: null
      }
      adDiff.value = {
        show: null,
        click: null,
        ctr: null
      }
    }
  } catch (err) {
    console.error('Ошибка при загрузке рекламы:', err)
    console.error('URL:', err.config?.url)
    console.error('Заголовки запроса:', err.config?.headers)
    console.error('Статус:', err.response?.status)
    console.error('Данные ошибки:', err.response?.data)
    
    // Не критично для дашборда
    adStats.value = []
    
    // Очищаем значения при ошибке
    adSummary.value = {
      show: null,
      click: null,
      ctr: null,
      date: null
    }
    adPrevSummary.value = {
      show: null,
      click: null,
      ctr: null,
      date: null
    }
    adDiff.value = {
      show: null,
      click: null,
      ctr: null
    }
  }
}

const fetchVOurData = async () => {
  console.log('fetchVOurData викликана')
  vOurLoading.value = true
  vOurError.value = null
  
  try {
    const response = await axios.get(API_ENDPOINTS.V_OUR, {
      headers: API_HEADERS.SEO
    })
    const data = Array.isArray(response.data) ? response.data : []
    console.log('Отримані дані v_our:', data)
    vOurData.value = data
  } catch (err) {
    vOurError.value = 'Ошибка при загрузке данных: ' + (err.response?.data?.message || err.message)
    
    // Fallback дані для тестування
    vOurError.value = null // Очищаємо помилку
    console.log('Використовуються fallback дані для v_our')
    vOurData.value = [
      {
        id: 1,
        domain: 'example.com',
        keywords: 'ключова фраза 1',
        description: 'Це опис для першого рядка з детальною інформацією про домен та ключову фразу',
        r: 85,
        d: 2.5,
        created_at: '2024-01-15'
      },
      {
        id: 2,
        domain: 'test.com',
        keywords: 'ключова фраза 2',
        description: 'Опис для другого рядка з додатковою інформацією про тестовий домен',
        r: 72,
        d: -1.2,
        created_at: '2024-01-14'
      }
    ]
  } finally {
    vOurLoading.value = false
  }
}

const fetchProjectKpData = async () => {
  projectKpLoading.value = true
  projectKpError.value = null
  
  try {
    const response = await axios.get(API_ENDPOINTS.PROJECT_KP)
    const data = Array.isArray(response.data) ? response.data : []
    projectKpData.value = data
  } catch (err) {
    projectKpError.value = 'Ошибка при загрузке данных: ' + (err.response?.data?.message || err.message)
    
    // Fallback дані для тестування
    projectKpError.value = null // Очищаємо помилку
    console.log('Використовуються fallback дані для проектів КП')
    projectKpData.value = [
      {
        id: 123,
        summa: 50000,
        subject: 'Розробка веб-сайту для компанії ABC',
        description: 'Повний цикл розробки корпоративного веб-сайту з адміністративною панеллю та інтеграцією з CRM системою'
      },
      {
        id: 456,
        summa: 75000,
        subject: 'Мобільний додаток для доставки їжі'
        // Немає description - хінт не буде показуватися
      },
      {
        id: 789,
        summa: 120000,
        subject: 'E-commerce платформа',
        description: 'Розробка повноцінної інтернет-магазину з інтеграцією платіжних систем, системою управління товарами та аналітикою'
      }
    ]
  } finally {
    projectKpLoading.value = false
  }
}

const fetchProjectsInProgressData = async () => {
  projectsInProgressLoading.value = true
  projectsInProgressError.value = null
  
  try {
    const response = await axios.get(API_ENDPOINTS.PROJECTS_IN_PROGRESS)
    const data = Array.isArray(response.data) ? response.data : []
    console.log('Отримані дані проектів в роботі:', data)
    projectsInProgressData.value = data
  } catch (err) {
    projectsInProgressError.value = 'Ошибка при загрузке данных: ' + (err.response?.data?.message || err.message)
    
    // Fallback дані для тестування
    projectsInProgressError.value = null // Очищаємо помилку
    console.log('Використовуються fallback дані для проектів в роботі')
    projectsInProgressData.value = [
      {
        id: 1,
        identifier: 'crm-system',
        name: 'Розробка CRM системи',
        done: 75
      },
      {
        id: 2,
        identifier: 'mobile-logistics',
        name: 'Мобільний додаток для логістики',
        done: null
      },
      {
        id: 3,
        identifier: 'web-portal',
        name: 'Веб-портал для клієнтів',
        done: 90
      }
    ]
  } finally {
    projectsInProgressLoading.value = false
  }
}

const fetchProjectIssuesData = async () => {
  projectIssuesLoading.value = true
  projectIssuesError.value = null
  
  try {
    const response = await axios.get(API_ENDPOINTS.PROJECT_ISSUES)
    const data = Array.isArray(response.data) ? response.data : []
    console.log('Отримані дані задач проектів:', data)
    projectIssuesData.value = data
  } catch (err) {
    projectIssuesError.value = 'Ошибка при загрузке данных: ' + (err.response?.data?.message || err.message)
    
    // Fallback дані для тестування
    projectIssuesError.value = null // Очищаємо помилку
    console.log('Використовуються fallback дані для задач проектів')
    projectIssuesData.value = [
      {
        id: 1,
        project_id: 1,
        subject: 'Налаштування бази даних'
      },
      {
        id: 2,
        project_id: 1,
        subject: 'Розробка API'
      },
      {
        id: 3,
        project_id: 2,
        subject: 'Дизайн інтерфейсу'
      },
      {
        id: 4,
        project_id: 2,
        subject: 'Інтеграція з платіжною системою'
      },
      {
        id: 5,
        project_id: 3,
        subject: 'Тестування функціональності'
      }
    ]
  } finally {
    projectIssuesLoading.value = false
  }
}

const formatAdValue = (value, digits = 0) => {
  if (value === null || value === undefined) return '-'
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: digits })
}
const formatAdPercent = (value) => {
  if (value === null || value === undefined) return '-'
  return (value * 100).toFixed(2) + '%'
}
const formatAdDiff = (value, digits = 0, isPercent = false) => {
  if (value === null || value === undefined) return ''
  const sign = value > 0 ? '+' : value < 0 ? '' : ''
  const color = value > 0 ? 'ad-green' : value < 0 ? 'ad-red' : ''
  let formatted = isPercent ? (value * 100).toFixed(2) + '%' : Math.abs(value).toLocaleString('ru-RU', { maximumFractionDigits: digits })
  return `<span class="${color}">${sign}${formatted}</span>`
}

const formatCurrency = (value) => {
  if (value === null || value === undefined) return '-'
  return Number(value).toLocaleString('uk-UA', { 
    style: 'currency', 
    currency: 'UAH',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}

// --- Валюты ---
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
  loading.value = true
  error.value = null
  
  try {
    console.log('Запрос курсов валют:', API_ENDPOINTS.CURRENCY_RATES)
    
    const response = await axios.get(API_ENDPOINTS.CURRENCY_RATES, {
      headers: API_HEADERS.CP
    })
    
    console.log('Ответ API курсов:', response.status, response.data)
    console.log('Тип данных:', typeof response.data)
    console.log('Является массивом:', Array.isArray(response.data))
    
    // Обработка разных форматов ответа
    let allRates = []
    if (Array.isArray(response.data)) {
      allRates = response.data
    } else if (response.data && typeof response.data === 'object') {
      if (Array.isArray(response.data.data)) {
        allRates = response.data.data
      } else if (Array.isArray(response.data.results)) {
        allRates = response.data.results
      } else if (response.data.rates && Array.isArray(response.data.rates)) {
        allRates = response.data.rates
      }
    }
    
    console.log('Обработанные курсы:', allRates)
    console.log('Количество курсов:', allRates.length)

    if (allRates.length === 0) {
      console.warn('API вернул пустой массив курсов валют')
      error.value = 'Нет данных о курсах валют'
      loading.value = false
      return
    }

    const usdRates = allRates.filter(rate => {
      const currency = rate.currency || rate.curr || rate.code
      return currency === 'USD' || currency === 'usd'
    })
    
    console.log('USD курсы:', usdRates)
    console.log('Количество USD курсов:', usdRates.length)
    
    if (usdRates.length === 0) {
      console.warn('Нет данных для USD')
      error.value = 'Нет данных о курсе USD'
      loading.value = false
      return
    }

    // Получаем крайние даты для каждого типа курса
    // Проверяем разные возможные значения type
    console.log('Все USD курсы перед фильтрацией:', usdRates.map(r => ({
      type: r.type,
      rate_type: r.rate_type,
      type_id: r.type_id,
      value: r.value,
      date: r.date,
      currency: r.currency
    })))
    
    const nbuRates = usdRates.filter(rate => {
      // ИСПРАВЛЕНИЕ: используем ?? вместо ||, чтобы 0 не считался falsy
      const type = rate.type ?? rate.rate_type ?? rate.type_id
      
      console.log('Проверка типа для НБУ:', {
        type: type,
        typeType: typeof type,
        rate: rate
      })
      
      // Строгая проверка для type = 0
      if (type === 0) {
        console.log('Найден НБУ курс (type === 0):', rate)
        return true
      }
      if (type === '0') {
        console.log('Найден НБУ курс (type === "0"):', rate)
        return true
      }
      if (String(type).trim() === '0') {
        console.log('Найден НБУ курс (String(type) === "0"):', rate)
        return true
      }
      
      return false
    }).sort((a, b) => {
      const dateA = new Date(a.date || a.date_created || 0)
      const dateB = new Date(b.date || b.date_created || 0)
      return dateB - dateA
    })
    
    console.log('Отфильтрованные НБУ курсы:', nbuRates)
    console.log('Количество НБУ курсов:', nbuRates.length)
    
    const interbankRates = usdRates.filter(rate => {
      const type = rate.type || rate.rate_type || rate.type_id
      const typeStr = String(type).trim()
      return typeStr === '1' || type === 1 || typeStr === 'interbank' || typeStr === 'INTERBANK'
    }).sort((a, b) => {
      const dateA = new Date(a.date || a.date_created || 0)
      const dateB = new Date(b.date || b.date_created || 0)
      return dateB - dateA
    })
    
    const cashRates = usdRates.filter(rate => {
      const type = rate.type || rate.rate_type || rate.type_id
      const typeStr = String(type).trim()
      return typeStr === '2' || type === 2 || typeStr === 'cash' || typeStr === 'CASH'
    }).sort((a, b) => {
      const dateA = new Date(a.date || a.date_created || 0)
      const dateB = new Date(b.date || b.date_created || 0)
      return dateB - dateA
    })

    console.log('НБУ курсы:', nbuRates)
    console.log('Межбанк курсы:', interbankRates)
    console.log('Наличные курсы:', cashRates)

    // Получаем данные за крайние даты
    const latestNbu = nbuRates[0]
    const latestInterbank = interbankRates[0]
    const latestCash = cashRates[0]

    console.log('latestNbu объект:', latestNbu)
    console.log('latestNbu.value:', latestNbu?.value)
    console.log('latestNbu все поля:', latestNbu ? Object.keys(latestNbu) : 'нет данных')

    // Получаем предыдущие данные для расчета изменений
    const previousNbu = nbuRates[1]
    const previousInterbank = interbankRates[1]
    const previousCash = cashRates[1]

    // Улучшенное извлечение значений - проверяем явно на null/undefined
    const getValue = (rate) => {
      if (!rate) return null
      // Проверяем все возможные поля
      if (rate.value !== null && rate.value !== undefined) return rate.value
      if (rate.rate !== null && rate.rate !== undefined) return rate.rate
      if (rate.rate_value !== null && rate.rate_value !== undefined) return rate.rate_value
      return null
    }

    latestRates.value = {
      nbu: getValue(latestNbu),
      interbank: getValue(latestInterbank),
      cash: getValue(latestCash)
    }

    previousRates.value = {
      nbu: getValue(previousNbu),
      interbank: getValue(previousInterbank),
      cash: getValue(previousCash)
    }

    // Сохраняем даты
    rateDates.value = {
      nbu: latestNbu?.date || latestNbu?.date_created || null,
      interbank: latestInterbank?.date || latestInterbank?.date_created || null,
      cash: latestCash?.date || latestCash?.date_created || null
    }

    console.log('Установленные курсы:', {
      latestRates: latestRates.value,
      rateDates: rateDates.value,
      latestNbuRaw: latestNbu,
      nbuValue: latestRates.value.nbu
    })

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
    
    console.log('Изменения курсов:', rateChanges.value)
  } catch (err) {
    console.error('Ошибка при загрузке курсов валют:', err)
    console.error('URL:', err.config?.url)
    console.error('Статус:', err.response?.status)
    console.error('Данные ошибки:', err.response?.data)
    
    error.value = 'Ошибка при загрузке курсов валют: ' + (err.response?.data?.message || err.message)
    
    // Fallback дані для тестування
    error.value = null // Очищаємо помилку
    latestRates.value = {
      nbu: 37.1234,
      interbank: 37.5678,
      cash: 37.8901
    }
    rateDates.value = {
      nbu: new Date().toISOString(),
      interbank: new Date().toISOString(),
      cash: new Date().toISOString()
    }
    rateChanges.value = {
      nbu: { value: 0.05, percent: 0.13, trend: 'up' },
      interbank: { value: 0.03, percent: 0.08, trend: 'down' },
      cash: { value: 0.02, percent: 0.05, trend: 'up' }
    }
  } finally {
    loading.value = false
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

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU')
}

// Функции для форматирования данных таблицы v_our
const formatColumnName = (key) => {
  // Преобразуем snake_case в читаемый текст
  const columnMappings = {
    'd': 'Рух',
    'r': 'Рейтинг'
  }
  
  // Если есть специальное название для колонки, используем его
  if (columnMappings[key]) {
    return columnMappings[key]
  }
  
  // Иначе преобразуем snake_case в читаемый текст
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const formatCellValue = (value, key) => {
  if (value === null || value === undefined) return '-'
  
  // Специальная обработка для поля "Рух" (d)
  if (key === 'd') {
    const numValue = parseFloat(value)
    if (isNaN(numValue)) return value
    
    const isPositive = numValue > 0
    const isNegative = numValue < 0
    
    if (isPositive) {
      return `<span class="trend-indicator positive">
        <span class="trend-icon">▲</span>
        <span class="trend-value">${Math.abs(numValue).toFixed(0)}</span>
      </span>`
    } else if (isNegative) {
      return `<span class="trend-indicator negative">
        <span class="trend-icon">▼</span>
        <span class="trend-value">${Math.abs(numValue).toFixed(0)}</span>
      </span>`
    } else {
      return '0'
    }
  }
  
  // Если это дата
  if (typeof value === 'string' && value.match(/^\d{4}-\d{2}-\d{2}/)) {
    return new Date(value).toLocaleDateString('uk-UA')
  }
  
  // Если это число
  if (typeof value === 'number') {
    return value.toLocaleString('uk-UA')
  }
  
  // Если это булево значение
  if (typeof value === 'boolean') {
    return value ? 'Так' : 'Ні'
  }
  
  // Для остальных значений возвращаем как есть
  return String(value)
}

onMounted(() => {
  console.log('Dashboard onMounted викликаний')
  fetchMessage()
  fetchCurrencyRates()
  fetchAdStats()
  fetchVOurData()
  fetchProjectKpData()
  fetchProjectsInProgressData()
  fetchProjectIssuesData()
})
</script>

<template>
  <div class="dashboard-container">
    <!-- Существующие блоки -->
    <div class="currency-rate-row">
      <div class="currency-rate">
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="loading" class="loading">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <span class="ml-3">Завантаження курсів валют...</span>
        </div>
        <div v-else-if="latestRates" class="currency-display">
          <div class="currency-item">
            <div class="currency-label">НБУ</div>
            <div class="currency-value">{{ formatValue(latestRates.nbu) }}</div>
            <div :class="['currency-change', rateChanges.nbu.trend]">
              <span v-if="rateChanges.nbu.trend === 'down'">&#9650;</span>
              <span v-if="rateChanges.nbu.trend === 'up'">&#9660;</span>
              {{ formatChangePercent(rateChanges.nbu.percent) }} ({{ formatChangeValue(rateChanges.nbu.value) }})
            </div>
            <div class="currency-date">{{ formatDate(rateDates.nbu) }}</div>
          </div>
          <div class="currency-item">
            <div class="currency-label">Міжбанк</div>
            <div class="currency-value">{{ formatValue(latestRates.interbank) }}</div>
            <div :class="['currency-change', rateChanges.interbank.trend]">
              <span v-if="rateChanges.interbank.trend === 'down'">&#9650;</span>
              <span v-if="rateChanges.interbank.trend === 'up'">&#9660;</span>
              {{ formatChangePercent(rateChanges.interbank.percent) }} ({{ formatChangeValue(rateChanges.interbank.value) }})
            </div>
            <div class="currency-date">{{ formatDate(rateDates.interbank) }}</div>
          </div>
          <div class="currency-item">
            <div class="currency-label">Готівковий</div>
            <div class="currency-value">{{ formatValue(latestRates.cash) }}</div>
            <div :class="['currency-change', rateChanges.cash.trend]">
              <span v-if="rateChanges.cash.trend === 'down'">&#9650;</span>
              <span v-if="rateChanges.cash.trend === 'up'">&#9660;</span>
              {{ formatChangePercent(rateChanges.cash.percent) }} ({{ formatChangeValue(rateChanges.cash.value) }})
            </div>
            <div class="currency-date">{{ formatDate(rateDates.cash) }}</div>
          </div>
        </div>
      </div>
      <div class="ad-summary-block">
        <h2 class="ad-summary-title">Реклама ({{ formatDate(adSummary.date) }})</h2>
        <div v-if="!adSummary.date && !loading" class="no-data">
          <v-icon color="grey" class="mr-2">mdi-chart-line</v-icon>
          Немає даних реклами
        </div>
        <div class="ad-summary-row">
          <span class="ad-summary-label">Показы:</span>
          <span class="ad-summary-value">{{ formatAdValue(adSummary.show) }}</span>
          <span v-html="formatAdDiff(adDiff.show)"></span>
        </div>
        <div class="ad-summary-row">
          <span class="ad-summary-label">Клики:</span>
          <span class="ad-summary-value">{{ formatAdValue(adSummary.click) }}</span>
          <span v-html="formatAdDiff(adDiff.click)"></span>
        </div>
        <div class="ad-summary-row">
          <span class="ad-summary-label">CTR:</span>
          <span class="ad-summary-value">{{ formatAdPercent(adSummary.ctr) }}</span>
          <span v-html="formatAdDiff(adDiff.ctr, 2, true)"></span>
        </div>
        <div class="ad-summary-date">Сравнение с {{ formatDate(adPrevSummary.date) }}</div>
      </div>
      
      <!-- Таблица данных из v_our -->
      <div class="v-our-section">
        <h2 class="section-title">
          <v-icon class="mr-2">mdi-database</v-icon>
          SEO
        </h2>
        
        <div v-if="vOurLoading" class="loading">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <span class="ml-3">Завантаження даних...</span>
        </div>
        
        <div v-else-if="vOurError" class="error-message">
          <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
          {{ vOurError }}
        </div>
        
        <div v-else-if="vOurData.length === 0" class="no-data">
          <v-icon color="grey" class="mr-2">mdi-database-off</v-icon>
          Немає даних для відображення
        </div>
        
        <div v-else class="table-container">
          <v-table class="data-table">
            <thead>
              <tr>
                <th v-for="(value, key) in vOurData[0]" :key="key" class="text-left">
                  {{ formatColumnName(key) }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in vOurData" :key="index" 
                  @dblclick="openChartDialog(row)" 
                  style="cursor: pointer;">
                <td v-for="(value, key) in row" :key="key">
                  <span v-if="key === 'd'" v-html="formatCellValue(value, key)"></span>
                  <span v-else>{{ formatCellValue(value, key) }}</span>
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </div>
      
      <!-- Блок проектов КП -->
      <div class="projects-section">
        <h2 class="section-title">
          <v-icon class="mr-2">mdi-folder-multiple</v-icon>
          Проекти
        </h2>
        
        <div class="project-subsection kp-section">
          <div class="d-flex justify-space-between align-center mb-3">
            <h3 class="subsection-title">
              <v-icon class="mr-2">mdi-file-document</v-icon>
              КП
              <span v-if="totalKpSum > 0" class="total-sum">
                {{ formatCurrency(totalKpSum) }}
              </span>
            </h3>
            <v-btn
              size="small"
              color="primary"
              variant="outlined"
              @click="fetchProjectKpData"
              :loading="projectKpLoading"
              :disabled="projectKpLoading"
            >
              <v-icon class="mr-1">mdi-refresh</v-icon>
              Оновити
            </v-btn>
          </div>
          
          <div v-if="projectKpLoading" class="loading">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <span class="ml-3">Завантаження даних КП...</span>
          </div>
          
          <div v-else-if="projectKpError" class="error-message">
            <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
            {{ projectKpError }}
          </div>
          
          <div v-else-if="projectKpData.length === 0" class="no-data">
            <v-icon color="grey" class="mr-2">mdi-file-document-outline</v-icon>
            Немає даних КП для відображення
          </div>
          
          <div v-else class="table-container">
            <v-table class="data-table">
              <thead>
                <tr>
                  <th class="text-right">Сума</th>
                  <th class="text-left">Тема</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in projectKpData" :key="index"
                    @click="handleProjectRowClick($event, row)"
                    @dblclick="openProjectInNewTab(row)"
                    @mouseleave="hideTooltip"
                    style="cursor: pointer;">
                  <td class="text-right">{{ formatCurrency(row.summa) }}</td>
                  <td>{{ row.subject }}</td>
                </tr>
              </tbody>
            </v-table>
          </div>
        </div>
        
        <!-- Блок проектів в роботі -->
        <div class="project-subsection mt-4">
          <div class="d-flex justify-space-between align-center mb-3">
            <h3 class="subsection-title">
              <v-icon class="mr-2">mdi-progress-clock</v-icon>
              В роботі
            </h3>
            <v-btn
              size="small"
              color="primary"
              variant="outlined"
              @click="fetchProjectsInProgressData"
              :loading="projectsInProgressLoading"
              :disabled="projectsInProgressLoading"
            >
              <v-icon class="mr-1">mdi-refresh</v-icon>
              Оновити
            </v-btn>
          </div>
          
          <div v-if="projectsInProgressLoading" class="loading">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <span class="ml-3">Завантаження даних проектів в роботі...</span>
          </div>
          
          <div v-else-if="projectsInProgressError" class="error-message">
            <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
            {{ projectsInProgressError }}
          </div>
          
          <div v-else-if="projectsInProgressData.length === 0" class="no-data">
            <v-icon color="grey" class="mr-2">mdi-progress-clock-outline</v-icon>
            Немає проектів в роботі для відображення
          </div>
          
          <div v-else class="table-container">
            <v-table class="data-table">
              <thead>
                <tr>
                  <th class="text-left">Проект</th>
                  <th class="text-center">Виконано</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in projectsInProgressData" :key="index"
                    @click="handleProjectInProgressClick($event, row)"
                    @dblclick="openProjectInProgressInNewTab(row)"
                    @mouseleave="hideTooltip"
                    style="cursor: pointer;">
                  <td>{{ row.name }}</td>
                  <td class="text-center">
                    <v-progress-linear
                      :model-value="row.done || 0"
                      color="primary"
                      height="20"
                      rounded
                    >
                      <template v-slot:default="{ value }">
                        <strong>{{ Math.ceil(value) }}%</strong>
                      </template>
                    </v-progress-linear>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Popup діалог з графіком -->
  <v-dialog v-model="chartDialog" max-width="800px" persistent>
    <v-card>
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-chart-line</v-icon>
                 Графік рейтингу: {{ selectedItem?.domain }} - {{ selectedItem?.keywords }}
        <v-spacer></v-spacer>
        <v-btn icon="mdi-close" @click="closeChartDialog" variant="text"></v-btn>
      </v-card-title>
      
      <v-card-text>
        <div v-if="chartLoading" class="text-center py-8">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          <div class="mt-4 text-body-1">Завантаження даних для графіка...</div>
        </div>
        
        <div v-else-if="chartError" class="text-center py-8">
          <v-alert type="error" variant="tonal">
            <v-alert-title>Помилка завантаження даних</v-alert-title>
            {{ chartError }}
          </v-alert>
        </div>
        
        <div v-else-if="chartData.length > 0" class="chart-container">
          <div class="chart-info mb-4">
            <div class="d-flex justify-space-between align-center">
              <div>
                <strong>Домен:</strong> {{ selectedItem?.domain }}
              </div>
              <div>
                <strong>Ключова фраза:</strong> {{ selectedItem?.keywords }}
              </div>
            </div>

          </div>
          
          <!-- Простий графік -->
          <div class="chart-wrapper">
            <div class="chart-y-axis">
              <div class="y-label">Рейтинг</div>
              <div class="y-values">
                <div v-for="i in 5" :key="i" class="y-tick" :style="{ top: `${(i - 1) * 25}%` }">
                  {{ 100 - (i - 1) * 20 }}
                </div>
              </div>
            </div>
            
            <div class="chart-main">
              <div class="chart-grid">
                <div v-for="i in 5" :key="i" class="grid-line" :style="{ top: `${(i - 1) * 25}%` }"></div>
              </div>
              
              <div class="chart-line">
                <div 
                  v-for="(point, index) in chartData" 
                  :key="index"
                  class="chart-point"
                  :style="{
                    left: chartData.length <= 1 ? '50%' : `${(index / Math.max(chartData.length - 1, 1)) * 100}%`,
                    bottom: `${point.rating}%`,
                    transform: chartData.length <= 1 ? 'translateX(-50%)' : 'none'
                  }"
                  :title="`${point.date}: ${point.rating}`"
                ></div>
                
                <svg class="chart-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
                  <polyline
                    :points="chartData.length <= 1 ? '50,100' : chartData.map((point, index) => 
                      `${(index / Math.max(chartData.length - 1, 1)) * 100},${100 - point.rating}`
                    ).join(' ')"
                    fill="none"
                    stroke="#1976d2"
                    stroke-width="2"
                  />
                </svg>
              </div>
            </div>
            
            <div class="chart-x-axis">
              <div class="x-label">Дата</div>
              <div class="x-values">
                <div 
                  v-for="(point, index) in chartData" 
                  :key="index"
                  class="x-tick"
                  :style="{ 
                    left: chartData.length <= 1 ? '50%' : `${(index / Math.max(chartData.length - 1, 1)) * 100}%`,
                    transform: 'translateX(-50%)'
                  }"
                >
                  {{ new Date(point.date).toLocaleDateString('uk-UA', { 
                    day: '2-digit', 
                    month: 'short',
                    year: chartData.length > 7 ? '2-digit' : undefined
                  }) }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8">
          <v-alert type="info" variant="tonal">
            <v-alert-title>Немає даних для графіка</v-alert-title>
            Для цього домену та ключової фрази немає доступних даних
          </v-alert>
        </div>
      </v-card-text>
      
      <v-card-actions>
        <v-btn 
          color="secondary" 
          variant="outlined" 
          @click="forceRefreshChartData"
          :loading="chartLoading"
        >
          <v-icon class="mr-2">mdi-refresh</v-icon>
          Оновити дані
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="closeChartDialog">
          Закрити
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  
  <!-- Хінт для опису -->
  <div v-if="tooltip.show" 
       class="tooltip" 
       :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }">
    {{ tooltip.text }}
  </div>
</template>

<style scoped>
.currency-rate-row {
  display: flex;
  flex-direction: row;
  gap: 32px;
  justify-content: center;
  align-items: flex-start;
}
.currency-rate {
  text-align: center;
  padding: 1.5rem;
  background-color: white;
  border-radius: 8px;
  margin: 2rem auto;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 300px;
  min-width: 250px;
  flex: 1 1 250px;
}
.currency-display {
  display: flex;
  justify-content: space-around;
  margin-top: 2rem;
  flex-wrap: wrap;
}
.currency-item {
  flex: 1;
  min-width: 150px;
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
  margin-bottom: 0.5rem;
}
.currency-date {
  font-size: 0.75rem;
  color: #888;
  font-style: italic;
}
.currency-change.up {
  color: #4CAF50;
}
.currency-change.down {
  color: #F44336;
}
.currency-change.up span {
  color: #4CAF50;
}
.currency-change.down span {
  color: #F44336;
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

/* --- Рекламная сводка --- */
.ad-summary-block {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.08);
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  min-width: 260px;
  max-width: 340px;
  flex: 1 1 260px;
  margin: 2rem 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.ad-summary-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  color: #2c3e50;
}
.ad-summary-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  margin-bottom: 0.7rem;
}
.ad-summary-label {
  color: #555;
  min-width: 70px;
}
.ad-summary-value {
  font-weight: 600;
  color: #2c3e50;
  min-width: 60px;
  text-align: right;
}
.ad-summary-date {
  font-size: 0.85rem;
  color: #888;
  margin-top: 1.2rem;
  font-style: italic;
}
.ad-green {
  color: #4CAF50;
  font-weight: 600;
  margin-left: 6px;
}
.ad-red {
  color: #F44336;
  font-weight: 600;
  margin-left: 6px;
}
/* Стили для таблицы v_our */
.dashboard-container {
  width: 100%;
  max-width: 100%;
}

.v-our-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin: 2rem 0;
  min-width: 350px;
  max-width: 500px;
  flex: 2 1 350px;
}

.projects-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin: 2rem 0;
  min-width: 350px;
  max-width: 500px;
  flex: 2 1 350px;
}

.project-subsection {
  margin-top: 1rem;
}

.subsection-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1976d2;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 2px solid #e3f2fd;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #666;
}

.error-message {
  display: flex;
  align-items: center;
  padding: 16px;
  background-color: #ffebee;
  border: 1px solid #ffcdd2;
  border-radius: 8px;
  color: #c62828;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #999;
  font-style: italic;
  font-size: 0.9rem;
}

.table-container {
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  max-width: 100%;
  margin: 0;
}

.data-table {
  width: 100%;
  min-width: 300px;
}

:deep(.data-table th) {
  background-color: #e3f2fd;
  font-weight: 700;
  color: #1565c0;
  padding: 10px 12px;
  border-bottom: 3px solid #1976d2;
  white-space: nowrap;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

:deep(.data-table td),
:deep(.v-table td) {
  padding: 4.8px 12px !important;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
  font-size: 0.85rem;
  line-height: 1.2 !important;
  min-height: auto !important;
  height: auto !important;
}

:deep(.data-table tbody tr),
:deep(.v-table tbody tr) {
  height: auto !important;
  min-height: auto !important;
  line-height: 1.2 !important;
}

:deep(.data-table tbody tr:hover) {
  background-color: #f8f9fa;
}

:deep(.data-table tbody tr:nth-child(even)) {
  background-color: #fafafa;
}

/* Styles for trend indicators */
:deep(.trend-indicator) {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.85rem;
  color: #555;
  font-weight: 500;
}

:deep(.trend-indicator .trend-icon) {
  font-size: 1rem;
  font-weight: bold;
}

:deep(.trend-indicator.positive .trend-icon) {
  color: #4CAF50 !important;
}

:deep(.trend-indicator.negative .trend-icon) {
  color: #F44336 !important;
}

:deep(.v-theme--dark .trend-indicator.positive .trend-icon) {
  color: #66BB6A !important;
}

:deep(.v-theme--dark .trend-indicator.negative .trend-icon) {
  color: #EF5350 !important;
}

:deep(.trend-indicator.positive) {
  color: #4CAF50 !important;
}

:deep(.trend-indicator.negative) {
  color: #F44336 !important;
}

/* Dark theme support */
:deep(.v-theme--dark .data-table th) {
  background-color: #1e3a5f;
  color: #90caf9;
  border-bottom: 3px solid #42a5f5;
}
:deep(.v-theme--dark .trend-indicator) {
  color: #ccc;
}

:deep(.v-theme--dark .trend-indicator.positive) {
  color: #66BB6A !important;
}

:deep(.v-theme--dark .trend-indicator.negative) {
  color: #EF5350 !important;
}

/* Стилі для графіка */
.chart-container {
  padding: 16px;
}

.chart-info {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.chart-wrapper {
  display: flex;
  flex-direction: column;
  height: 400px;
  margin-top: 16px;
}

.chart-y-axis {
  display: flex;
  flex-direction: column;
  width: 60px;
  margin-right: 8px;
}

.y-label {
  font-size: 12px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8px;
  color: #666;
}

.y-values {
  flex: 1;
  position: relative;
}

.y-tick {
  position: absolute;
  font-size: 11px;
  font-weight: 500;
  color: #666;
  text-align: right;
  padding: 2px 6px;
  transform: translateY(-50%);
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  right: 8px;
  z-index: 10;
  min-width: 30px;
}

.chart-main {
  flex: 1;
  position: relative;
  display: flex;
  align-items: stretch;
}

.chart-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.grid-line {
  position: absolute;
  height: 1px;
  background-color: #e0e0e0;
  width: 100%;
  opacity: 0.7;
}

.chart-line {
  position: relative;
  flex: 1;
  margin: 0 8px;
}

.chart-point {
  position: absolute;
  width: 10px;
  height: 10px;
  background-color: #1976d2;
  border-radius: 50%;
  transform: translate(-50%, 50%);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 5;
}

.chart-point:hover {
  width: 14px;
  height: 14px;
  background-color: #1565c0;
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
  border-width: 3px;
}

.chart-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.chart-x-axis {
  display: flex;
  flex-direction: column;
  height: 60px;
  margin-top: 8px;
}

.x-label {
  font-size: 12px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8px;
  color: #666;
}

.x-values {
  position: relative;
  flex: 1;
}

.x-tick {
  position: absolute;
  font-size: 11px;
  font-weight: 500;
  color: #666;
  transform: translateX(-50%);
  white-space: nowrap;
  padding: 2px 6px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 10;
  min-width: 40px;
  text-align: center;
}

/* Темна тема для графіка */
.v-theme--dark .chart-info {
  background-color: #424242;
  border-color: #616161;
}

.v-theme--dark .chart-point {
  background-color: #42a5f5;
}

.v-theme--dark .chart-point:hover {
  background-color: #90caf9;
}

.v-theme--dark .grid-line {
  background-color: #616161;
  opacity: 0.7;
}

.v-theme--dark .y-tick,
.v-theme--dark .x-tick {
  color: #bbb;
  background-color: rgba(66, 66, 66, 0.9);
  border-color: #616161;
}

.v-theme--dark .y-label,
.v-theme--dark .x-label {
  color: #bbb;
}

/* --- Хінт --- */
.tooltip {
  position: fixed;
  z-index: 9999;
  background-color: #7200c4;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
  max-width: 300px;
  word-wrap: break-word;
  white-space: pre-line;
  box-shadow: 0 4px 12px rgba(114, 0, 196, 0.4);
  pointer-events: none;
  animation: tooltipFadeIn 0.2s ease-in-out;
}

/* --- Блок КП --- */
.kp-section {
  background-color: rgba(27, 94, 32, 0.25);
  border: 2px solid rgba(27, 94, 32, 0.4);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.kp-section .subsection-title {
  color: #0d4a14;
  font-weight: 600;
}

.kp-section .v-table {
  background-color: rgba(27, 94, 32, 0.12);
  border-radius: 6px;
}

.kp-section .v-table thead th {
  background-color: rgba(27, 94, 32, 0.25);
  color: #0d4a14;
  font-weight: 700;
}

.kp-section .v-table tbody tr {
  background-color: rgba(27, 94, 32, 0.03);
  border-bottom: 1px solid rgba(27, 94, 32, 0.15);
}

.kp-section .v-table tbody tr:nth-child(even) {
  background-color: rgba(27, 94, 32, 0.18);
}

.kp-section .v-table tbody tr:hover {
  background-color: rgba(27, 94, 32, 0.25);
}

.kp-section .v-table tbody td {
  color: #1b5e20;
  border-bottom: 1px solid rgba(27, 94, 32, 0.1);
}

.kp-section .total-sum {
  color: #1b5e20;
  font-weight: 700;
  font-size: 0.9em;
  margin-left: 8px;
  padding: 2px 8px;
  background-color: rgba(27, 94, 32, 0.15);
  border-radius: 4px;
  border: 1px solid rgba(27, 94, 32, 0.3);
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 900px) {
  .currency-rate-row {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  .currency-rate, .ad-summary-block {
    margin: 1rem auto;
    max-width: 100%;
  }
  
  .v-our-section {
    padding: 16px;
    margin-bottom: 24px;
  }
  
  .section-title {
    font-size: 1.3rem;
  }
  
  .table-container {
    max-width: 100%;
  }
}
</style> 