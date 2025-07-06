from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Finance, Advertisement, SEO, Market, CP, CPCurrencyRate, MKStatGroup7d, StatUah7D, vUtm

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = '__all__'

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

class SEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEO
        fields = '__all__'

class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'

class CPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CP
        fields = '__all__'

class CPCurrencyRateSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(read_only=True)
    date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = CPCurrencyRate
        fields = ['date', 'currency', 'type', 'value', 'type_display']
        read_only_fields = ['date', 'currency', 'type']

class MKStatGroup7dSerializer(serializers.Serializer):
    d = serializers.DateField(format="%Y-%m-%d")
    campaign_name = serializers.CharField()
    show = serializers.IntegerField()
    clic = serializers.IntegerField()
    ctr = serializers.FloatField() 

class StatUah7DSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatUah7D
        fields = ['segments_date', 'uah']

class vUtmSerializer(serializers.ModelSerializer):
    class Meta:
        model = vUtm
        fields = '__all__'
