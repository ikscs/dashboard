from django.db import models
from django.contrib.auth.models import User

class Finance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        ordering = ['-date']

class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    campaign_name = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        ordering = ['-created_at']

class SEO(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    position = models.IntegerField()
    volume = models.IntegerField()
    difficulty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        ordering = ['-created_at']

class Market(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        ordering = ['-created_at']

class CP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        ordering = ['-created_at']

class ExternalData(models.Model):
    """
    Модель для работы с внешней базой данных
    """
    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'external_data'  # Префикс external_ для маршрутизации
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.external_id})"

class CPCurrencyRate(models.Model):
    pk = models.CompositePrimaryKey('date', 'currency', 'type')
    value = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField()
    currency = models.CharField(max_length=3)
    type = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'cp_currency_rate'
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'

    def __str__(self):
        return f"{self.date} - {self.currency} ({self.type})"

    @property
    def type_display(self):
        return dict(self.TYPE_CHOICES).get(self.type, self.type)

class MKStatGroup7dManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('mk_db')

class MKStatGroup7d(models.Model):
    """
    Модель для статистики по кампаниям за 7 дней из базы mk_db
    """
    d = models.DateField(verbose_name='Дата')
    campaign_name = models.CharField(max_length=255, verbose_name='Название кампании')
    show = models.IntegerField(verbose_name='Показы')
    clic = models.IntegerField(verbose_name='Клики')
    ctr = models.FloatField(verbose_name='CTR')

    objects = MKStatGroup7dManager()

    class Meta:
        managed = False
        db_table = 'stat_group_7d'
        verbose_name = 'Статистика кампании за 7 дней'
        verbose_name_plural = 'Статистика кампаний за 7 дней'
        ordering = ['-d', 'campaign_name']

    def __str__(self):
        return f"{self.d} - {self.campaign_name} (CTR: {self.ctr:.2f}%)"

class StatUah7D(models.Model):
    segments_date = models.DateField(primary_key=True, db_column='segments_date')
    uah = models.DecimalField(max_digits=10, decimal_places=2, db_column='uah')

    class Meta:
        managed = False  # Це View, Django не створює і не змінює його
        db_table = 'stat_uah_7d'  # ← заміни на точну назву view

    def __str__(self):
        return f"{self.segments_date} — {self.uah} грн"

class vUtm(models.Model):
    datetime = models.DateTimeField()
    ip = models.GenericIPAddressField()
    country = models.CharField(max_length=2)
    url = models.CharField(max_length=255)
    utm_source = models.CharField(max_length=100)
    utm_medium = models.CharField(max_length=50)
    utm_campaign = models.CharField(max_length=100)
    utm_coname = models.CharField(max_length=1)
    utm_content = models.CharField(max_length=100)
    utm_term = models.CharField(max_length=255)
    gclid = models.CharField(max_length=255)
    rest = models.CharField(max_length=255)
    id = models.BigIntegerField(primary_key=True)
    store = models.CharField(max_length=50)

    class Meta:
        managed = False  # бо таблиця вже існує
        db_table = 'gads"."v_utm'
