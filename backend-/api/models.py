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
