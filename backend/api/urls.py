from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'finances', views.FinanceViewSet)
router.register(r'advertisements', views.AdvertisementViewSet)
router.register(r'seo', views.SEOViewSet)
router.register(r'market', views.MarketViewSet)
router.register(r'cp', views.CPViewSet)
router.register(r'currency-rates', views.CPCurrencyRateViewSet)
router.register(r'stat-group-7d', views.MKStatGroup7dViewSet, basename='stat-group-7d')
router.register(r'stats-uah7d', views.StatUah7DViewSet, basename='stats-uah7d')
router.register(r'v-utm', views.vUtmViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', views.hello_world, name='hello'),
] 
