from django.db import models

class CurrencyRate(models.Model):
    currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.currency} - {self.rate} ({self.date})" 