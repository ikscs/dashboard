<template>
  <div class="settings-page">
    <v-card class="welcome-card">
      <v-card-title class="text-h4 mb-4">
        <v-icon size="large" class="mr-3">mdi-cog</v-icon>
        Налаштування
      </v-card-title>
      <v-card-text>
        <p class="text-body-1 mb-4">
          Добро пожаловать в раздел настроек! Здесь вы можете настроить параметры системы,
          управлять профилем и настройками безопасности.
        </p>
        
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-account</v-icon>
                Профиль
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Имя пользователя</v-list-item-title>
                    <v-list-item-subtitle>admin</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Email</v-list-item-title>
                    <v-list-item-subtitle>admin@example.com</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Роль</v-list-item-title>
                    <v-list-item-subtitle>Администратор</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-shield</v-icon>
                Безопасность
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Двухфакторная аутентификация</v-list-item-title>
                    <v-list-item-subtitle>Включена</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Последний вход</v-list-item-title>
                    <v-list-item-subtitle>Сегодня, 14:30</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>IP адрес</v-list-item-title>
                    <v-list-item-subtitle>192.168.1.100</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-row class="mt-4">
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-bell</v-icon>
                Уведомления
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Email уведомления</v-list-item-title>
                    <v-switch v-model="emailNotifications" color="primary"></v-switch>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Push уведомления</v-list-item-title>
                    <v-switch v-model="pushNotifications" color="primary"></v-switch>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>SMS уведомления</v-list-item-title>
                    <v-switch v-model="smsNotifications" color="primary"></v-switch>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-palette</v-icon>
                Внешний вид
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Тема</v-list-item-title>
                    <v-btn-toggle v-model="theme" mandatory>
                      <v-btn value="light">Светлая</v-btn>
                      <v-btn value="dark">Темная</v-btn>
                    </v-btn-toggle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Язык</v-list-item-title>
                    <v-select v-model="language" :items="languages" variant="outlined" density="compact"></v-select>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emailNotifications = ref(true)
const pushNotifications = ref(false)
const smsNotifications = ref(false)
const theme = ref('light')
const language = ref('ru')
const languages = ['ru', 'en', 'es', 'de']
</script>

<style scoped>
.settings-page {
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

.stat-card {
  transition: transform 0.2s ease-in-out;
  border-radius: 12px;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.v-list-item {
  padding: 8px 0;
}

.v-list-item-title {
  font-weight: 500;
}

.v-list-item-subtitle {
  color: rgba(var(--v-theme-on-surface), 0.7);
}
</style> 