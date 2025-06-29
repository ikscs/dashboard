<template>
  <div class="cp-page">
    <v-card class="welcome-card">
      <v-card-title class="text-h4 mb-4">
        <v-icon size="large" class="mr-3">mdi-account-group</v-icon>
        CP (Content Platform)
      </v-card-title>
      <v-card-text>
        <p class="text-body-1 mb-4">
          Добро пожаловать в раздел CP! Здесь вы можете управлять контентом,
          создавать публикации и отслеживать взаимодействие с аудиторией.
        </p>
        
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-file-document</v-icon>
                Публикации
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-primary">156</div>
                <div class="text-caption text-medium-emphasis">+12 за последний месяц</div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-eye</v-icon>
                Просмотры
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-success">2.1M</div>
                <div class="text-caption text-medium-emphasis">+25% к прошлому месяцу</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-row class="mt-4">
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-thumb-up</v-icon>
                Лайки
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-info">45.2K</div>
                <div class="text-caption text-medium-emphasis">За текущий месяц</div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-comment</v-icon>
                Комментарии
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-warning">8,947</div>
                <div class="text-caption text-medium-emphasis">За текущий месяц</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
// Логика компонента будет добавлена позже
</script>

<style scoped>
.cp-page {
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

.text-h3 {
  font-weight: 600;
  margin-bottom: 8px;
}

.text-caption {
  font-size: 0.875rem;
}
</style> 