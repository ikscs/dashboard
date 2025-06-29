import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import Finance from '../components/Finance.vue'
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
    component: () => import('../components/Advertisement.vue')
  },
  {
    path: '/seo',
    name: 'SEO',
    component: () => import('../components/SEO.vue')
  },
  {
    path: '/market',
    name: 'Market',
    component: () => import('../components/Market.vue')
  },
  {
    path: '/cp',
    name: 'CP',
    component: () => import('../components/CP.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../components/Settings.vue')
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