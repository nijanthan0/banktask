from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    dep = models.DecimalField(max_digits=20, decimal_places=2)
    unique_id = models.CharField(max_length=100, unique=True, default=None)
    is_active = models.CharField(max_length=100, default=1)

    def __str__(self):
        return self.name