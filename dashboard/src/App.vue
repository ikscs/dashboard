<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drawer = ref(true)
const rail = ref(true)
const theme = ref('light')

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

const toggleDrawer = () => {
  rail.value = !rail.value
}

const navigateTo = (path) => {
  router.push(path)
}
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
          prepend-icon="mdi-home"
          title="Главная"
          @click="navigateTo('/')"
        ></v-list-item>
        
        <v-list-item
          prepend-icon="mdi-cash-multiple"
          title="Финансы"
          @click="navigateTo('/finance')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-google-ads"
          title="Реклама"
          @click="navigateTo('/advertisement')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-magnify"
          title="SEO"
          @click="navigateTo('/seo')"
        ></v-list-item>

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
          prepend-icon="mdi-cog"
          title="Настройки"
          @click="navigateTo('/settings')"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      :elevation="1"
      class="app-bar"
    >
      <v-toolbar-title>Dashboard</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        :icon="theme === 'light' ? 'mdi-weather-night' : 'mdi-weather-sunny'"
        @click="toggleTheme"
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
  background-color: #f5f5f5 !important;
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
</style>
