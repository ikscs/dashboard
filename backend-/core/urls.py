from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from currency_rates.views import CurrencyRateViewSet, HelloView

router = routers.DefaultRouter()
router.register(r'currency-rates', CurrencyRateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/hello/', HelloView.as_view(), name='hello'),
] 