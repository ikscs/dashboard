from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from .models import Finance, Advertisement, SEO, Market, CP, CPCurrencyRate, MKStatGroup7d, vUtm
from .serializers import (
    FinanceSerializer, AdvertisementSerializer,
    SEOSerializer, MarketSerializer, CPSerializer, CPCurrencyRateSerializer, MKStatGroup7dSerializer, vUtmSerializer
)

from .models import StatUah7D
from .serializers import StatUah7DSerializer

# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({
        "message": "Привет, мир!",
        "status": "success"
    })

class FinanceViewSet(viewsets.ModelViewSet):
    serializer_class = FinanceSerializer
    permission_classes = [AllowAny]
    queryset = Finance.objects.all()

    def get_queryset(self):
        queryset = Finance.objects.all()
        
        # Фильтрация по дате
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
            
        return queryset.order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdvertisementViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]
    queryset = Advertisement.objects.all()

    def get_queryset(self):
        return Advertisement.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SEOViewSet(viewsets.ModelViewSet):
    serializer_class = SEOSerializer
    permission_classes = [IsAuthenticated]
    queryset = SEO.objects.all()

    def get_queryset(self):
        return SEO.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MarketViewSet(viewsets.ModelViewSet):
    serializer_class = MarketSerializer
    permission_classes = [IsAuthenticated]
    queryset = Market.objects.all()

    def get_queryset(self):
        return Market.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CPViewSet(viewsets.ModelViewSet):
    serializer_class = CPSerializer
    permission_classes = [IsAuthenticated]
    queryset = CP.objects.all()

    def get_queryset(self):
        return CP.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CPCurrencyRateViewSet(viewsets.ModelViewSet):
    serializer_class = CPCurrencyRateSerializer
    permission_classes = [AllowAny]
    queryset = CPCurrencyRate.objects.all()

    def get_queryset(self):
        queryset = CPCurrencyRate.objects.all()
        
        # Фильтрация по валюте
        currency = self.request.query_params.get('currency', None)
        if currency:
            queryset = queryset.filter(currency=currency)
            
        # Фильтрация по типу курса
        type = self.request.query_params.get('type', None)
        if type:
            queryset = queryset.filter(type=type)
            
        # Фильтрация по дате
        date_after = self.request.query_params.get('date_after', None)
        if date_after:
            queryset = queryset.filter(date__gte=date_after)
            
        date_before = self.request.query_params.get('date_before', None)
        if date_before:
            queryset = queryset.filter(date__lte=date_before)
            
        return queryset.order_by('-date')

class MKStatGroup7dViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для статистики кампаний за 7 дней (только чтение)
    """
    serializer_class = MKStatGroup7dSerializer
    permission_classes = [AllowAny]
    # Отключаем детальный просмотр, так как нет первичного ключа
    lookup_field = None

    def get_queryset(self):
        # Используем raw SQL для обхода проблемы с первичным ключом
        from django.db import connections
        with connections['mk_db'].cursor() as cursor:
            query = """
                SELECT d, campaign_name, show, clic, ctr 
                FROM stat_group_7d 
                ORDER BY d DESC, campaign_name
            """
            
            # Добавляем фильтры
            filters = []
            params = []
            
            campaign_name = self.request.query_params.get('campaign_name', None)
            if campaign_name:
                filters.append("campaign_name ILIKE %s")
                params.append(f'%{campaign_name}%')
                
            date_from = self.request.query_params.get('date_from', None)
            if date_from:
                filters.append("d >= %s")
                params.append(date_from)
                
            date_to = self.request.query_params.get('date_to', None)
            if date_to:
                filters.append("d <= %s")
                params.append(date_to)
                
            min_ctr = self.request.query_params.get('min_ctr', None)
            if min_ctr:
                filters.append("ctr >= %s")
                params.append(float(min_ctr))
                
            min_shows = self.request.query_params.get('min_shows', None)
            if min_shows:
                filters.append("show >= %s")
                params.append(int(min_shows))
            
            if filters:
                query = query.replace("ORDER BY", "WHERE " + " AND ".join(filters) + " ORDER BY")
            
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StatUah7DViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StatUah7D.objects.all().order_by('-segments_date')
    serializer_class = StatUah7DSerializer

class vUtmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vUtm.objects.all()
    serializer_class = vUtmSerializer
