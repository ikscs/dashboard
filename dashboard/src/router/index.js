import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import Finance from '../components/Finance.vue'
import Advertisement from '../components/Advertisement.vue'
import CurrencyRates from '../views/CurrencyRates.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HelloWorld
  },
  {
    path: '/finance',
    name: 'Finance',
    component: Finance
  },
  {
    path: '/advertisement',
    name: 'Advertisement',
    component: Advertisement
  },
  {
    path: '/currency-rates',
    name: 'currency-rates',
    component: CurrencyRates,
    meta: {
      title: 'Курсы валют',
      icon: 'mdi-currency-usd'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 