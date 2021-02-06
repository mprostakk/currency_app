from django.db import models
from django.conf import settings


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency_name = models.CharField(max_length=10, verbose_name='Currency')

    def __str__(self) -> str:
        return f'{self.user} - {self.currency_name}'
