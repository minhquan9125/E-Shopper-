from django.conf import settings
from django.db import models


class History(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=150)
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='id_user',
        related_name='purchase_history',
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price}'
