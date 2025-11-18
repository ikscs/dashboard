<template>
  <div class="projects-container">
    <v-card class="projects-card">
      <v-card-title class="projects-title">
        <v-icon class="mr-2">mdi-folder-multiple</v-icon>
        Проекти
      </v-card-title>
      
      <v-card-text>
        <div v-if="loading" class="loading-container">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
          ></v-progress-circular>
          <p class="mt-4">Завантаження проектів...</p>
        </div>
        
        <div v-else-if="error" class="error-container">
          <v-alert
            type="error"
            title="Помилка завантаження"
            :text="error"
            class="mb-4"
          ></v-alert>
          <v-btn
            color="primary"
            @click="fetchProjects"
            prepend-icon="mdi-refresh"
          >
            Спробувати ще раз
          </v-btn>
        </div>
        
        <div v-else-if="projects.length === 0" class="no-data-container">
          <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-folder-open</v-icon>
          <h3 class="text-h6 text-grey-darken-1">Немає доступних проектів</h3>
          <p class="text-body-2 text-grey">Проекти ще не додані або недоступні</p>
        </div>
        
        <div v-else class="projects-grid">
          <v-card
            v-for="project in projects"
            :key="project.id"
            class="project-card"
            elevation="2"
            @click="selectProject(project)"
          >
            <v-card-title class="project-card-title">
              <v-icon class="mr-2" :color="getProjectStatusColor(project.status)">
                {{ getProjectStatusIcon(project.status) }}
              </v-icon>
              {{ project.name }}
            </v-card-title>
            
            <v-card-text class="project-card-content">
              <p class="project-description">{{ project.description }}</p>
              
              <div class="project-meta">
                <v-chip
                  :color="getProjectStatusColor(project.status)"
                  size="small"
                  class="mr-2"
                >
                  {{ getProjectStatusText(project.status) }}
                </v-chip>
                
                <v-chip
                  v-if="project.priority"
                  :color="getPriorityColor(project.priority)"
                  size="small"
                >
                  {{ getPriorityText(project.priority) }}
                </v-chip>
              </div>
              
              <div class="project-dates">
                <div class="date-item">
                  <span class="date-label">Створено:</span>
                  <span class="date-value">{{ formatDate(project.created_at) }}</span>
                </div>
                <div v-if="project.deadline" class="date-item">
                  <span class="date-label">Дедлайн:</span>
                  <span class="date-value" :class="{ 'deadline-warning': isDeadlineNear(project.deadline) }">
                    {{ formatDate(project.deadline) }}
                  </span>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'

const projects = ref([])
const loading = ref(true)
const error = ref(null)

const fetchProjects = async () => {
  loading.value = true
  error.value = null
  
  try {
    console.log('Завантаження проектів...')
    // TODO: Замінити на реальний API endpoint коли він буде доступний
    // const response = await axios.get(API_ENDPOINTS.PROJECTS)
    // projects.value = response.data
    
    // Тимчасові тестові дані
    await new Promise(resolve => setTimeout(resolve, 1000)) // Імітація завантаження
    
    projects.value = [
      {
        id: 1,
        name: 'Розробка веб-сайту',
        description: 'Створення корпоративного веб-сайту з сучасним дизайном та функціональністю',
        status: 'active',
        priority: 'high',
        created_at: '2024-01-15',
        deadline: '2024-03-15'
      },
      {
        id: 2,
        name: 'Мобільний додаток',
        description: 'Розробка iOS та Android додатку для клієнтів',
        status: 'planning',
        priority: 'medium',
        created_at: '2024-02-01',
        deadline: '2024-05-01'
      },
      {
        id: 3,
        name: 'Система аналітики',
        description: 'Впровадження системи збору та аналізу даних',
        status: 'completed',
        priority: 'low',
        created_at: '2023-12-01',
        deadline: '2024-01-31'
      },
      {
        id: 4,
        name: 'Оновлення інфраструктури',
        description: 'Модернізація серверної інфраструктури та безпеки',
        status: 'active',
        priority: 'high',
        created_at: '2024-01-20',
        deadline: '2024-02-28'
      }
    ]
    
    console.log('Проекти завантажено:', projects.value)
  } catch (err) {
    console.error('Помилка завантаження проектів:', err)
    error.value = 'Помилка при завантаженні проектів: ' + err.message
  } finally {
    loading.value = false
  }
}

const selectProject = (project) => {
  console.log('Обрано проект:', project)
  // TODO: Додати логіку для відкриття деталей проекту
}

const getProjectStatusColor = (status) => {
  const colors = {
    'active': 'success',
    'planning': 'warning',
    'completed': 'info',
    'paused': 'grey',
    'cancelled': 'error'
  }
  return colors[status] || 'grey'
}

const getProjectStatusIcon = (status) => {
  const icons = {
    'active': 'mdi-play-circle',
    'planning': 'mdi-clock-outline',
    'completed': 'mdi-check-circle',
    'paused': 'mdi-pause-circle',
    'cancelled': 'mdi-close-circle'
  }
  return icons[status] || 'mdi-help-circle'
}

const getProjectStatusText = (status) => {
  const texts = {
    'active': 'Активний',
    'planning': 'Планування',
    'completed': 'Завершено',
    'paused': 'Призупинено',
    'cancelled': 'Скасовано'
  }
  return texts[status] || 'Невідомо'
}

const getPriorityColor = (priority) => {
  const colors = {
    'high': 'error',
    'medium': 'warning',
    'low': 'success'
  }
  return colors[priority] || 'grey'
}

const getPriorityText = (priority) => {
  const texts = {
    'high': 'Високий',
    'medium': 'Середній',
    'low': 'Низький'
  }
  return texts[priority] || 'Невідомо'
}

const formatDate = (dateString) => {
  if (!dateString) return 'Не вказано'
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('uk-UA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (err) {
    return dateString
  }
}

const isDeadlineNear = (deadline) => {
  if (!deadline) return false
  
  try {
    const deadlineDate = new Date(deadline)
    const today = new Date()
    const diffTime = deadlineDate - today
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    return diffDays <= 7 && diffDays >= 0
  } catch (err) {
    return false
  }
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.projects-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.projects-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.projects-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1976d2;
  border-bottom: 2px solid #e3f2fd;
  padding-bottom: 16px;
}

.loading-container,
.error-container,
.no-data-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.project-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #1976d2;
}

.project-card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  padding-bottom: 8px;
}

.project-card-content {
  padding-top: 0;
}

.project-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.project-dates {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.date-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.date-label {
  color: #666;
  font-weight: 500;
}

.date-value {
  color: #333;
  font-weight: 600;
}

.deadline-warning {
  color: #f57c00 !important;
  font-weight: 700;
}

/* Responsive design */
@media (max-width: 768px) {
  .projects-container {
    padding: 10px;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .project-card {
    margin-bottom: 10px;
  }
}

/* Dark theme support */
.v-theme--dark .projects-card {
  background: #1e1e1e;
  color: #ffffff;
}

.v-theme--dark .project-card {
  background: #2d2d2d;
  border-color: #404040;
}

.v-theme--dark .project-card:hover {
  border-color: #1976d2;
  background: #333333;
}

.v-theme--dark .project-card-title {
  color: #ffffff;
}

.v-theme--dark .project-description {
  color: #b0b0b0;
}

.v-theme--dark .date-label {
  color: #b0b0b0;
}

.v-theme--dark .date-value {
  color: #ffffff;
}
</style> 