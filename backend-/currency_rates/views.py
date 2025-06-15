from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
import logging
from .models import CurrencyRate
from .serializers import CurrencyRateSerializer

logger = logging.getLogger(__name__)

class CurrencyRateViewSet(viewsets.ModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer

    def get_queryset(self):
        queryset = CurrencyRate.objects.all()
        
        # Получаем параметры фильтрации
        date_after = self.request.query_params.get('date_after')
        date_before = self.request.query_params.get('date_before')
        
        try:
            if date_after:
                date_after = parse_date(date_after)
                if date_after:
                    queryset = queryset.filter(date__gte=date_after)
            
            if date_before:
                date_before = parse_date(date_before)
                if date_before:
                    queryset = queryset.filter(date__lte=date_before)
                    
        except Exception as e:
            logger.error(f"Error parsing dates: {str(e)}")
            raise ValidationError("Неверный формат даты")
            
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"Validation error in CurrencyRateViewSet.list: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in CurrencyRateViewSet.list: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при получении курсов валют"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in CurrencyRateViewSet.create: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in CurrencyRateViewSet.create: {str(e)}")
            return Response(
                {"error": "Произошла ошибка при создании курса валюты"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"}) 