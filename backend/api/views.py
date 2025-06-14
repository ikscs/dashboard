from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Finance, Advertisement, SEO, Market, CP, CPCurrencyRate
from .serializers import (
    FinanceSerializer, AdvertisementSerializer,
    SEOSerializer, MarketSerializer, CPSerializer, CPCurrencyRateSerializer
)

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
