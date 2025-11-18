import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/Dashboard.vue'
import Finance from '../components/Finance.vue'
import CurrencyRates from '../views/CurrencyRates.vue'
import Projects from '../components/Projects.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Dashboard
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
    path: '/advertisement/queries',
    name: 'AdvertisementQueries',
    component: () => import('../components/AdvertisementQueries.vue')
  },
  {
    path: '/seo',
    name: 'SEO',
    component: () => import('../components/SEO.vue')
  },
  {
    path: '/seo/top',
    name: 'Top',
    component: () => import('../components/SEO.vue')
  },
  {
    path: '/seo/metatags',
    name: 'MetaTegs',
    component: () => import('../components/MetaTegs.vue')
  },
  {
    path: '/seo/metatags-check',
    name: 'MetaTegs_check',
    component: () => import('../components/MetaTegs_check.vue')
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
    path: '/projects',
    name: 'Projects',
    component: Projects
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../components/Settings.vue')
  },
  {
    path: '/help',
    name: 'Help',
    component: () => import('../components/Help.vue')
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