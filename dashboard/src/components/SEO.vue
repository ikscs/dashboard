<template>
  <div class="seo-page">
    <v-card class="welcome-card">
      <v-card-title class="text-h4 mb-4">
        <v-icon size="large" class="mr-3">mdi-magnify</v-icon>
        SEO
      </v-card-title>
      <v-card-text>
        <p class="text-body-1 mb-4">
          Добро пожаловать в раздел SEO! Здесь вы можете отслеживать позиции в поисковых системах,
          анализировать ключевые слова и оптимизировать видимость сайта.
        </p>
        
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-trending-up</v-icon>
                Позиции в топ-10
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-primary">47</div>
                <div class="text-caption text-medium-emphasis">+5 за последний месяц</div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-magnify</v-icon>
                Органический трафик
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-success">89.2K</div>
                <div class="text-caption text-medium-emphasis">+15% к прошлому месяцу</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-row class="mt-4">
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-key</v-icon>
                Ключевые слова
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-info">1,247</div>
                <div class="text-caption text-medium-emphasis">Отслеживается</div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="stat-card">
              <v-card-title class="text-h6">
                <v-icon class="mr-2">mdi-speedometer</v-icon>
                Скорость загрузки
              </v-card-title>
              <v-card-text>
                <div class="text-h3 text-warning">2.3s</div>
                <div class="text-caption text-medium-emphasis">Хорошо</div>
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
.seo-page {
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