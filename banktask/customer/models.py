from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=100)
    dep = models.DecimalField(max_digits=20, decimal_places=2)
    unique_id = models.CharField(max_length=100, unique=True, default=None)
    is_active = models.CharField(max_length=100, default=1)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Customer)
def pre_create_uniqueid(sender, instance, **kwargs):
    last_id = Customer.objects.all().last()
    if not last_id:
        last_id = 0
    else:
        last_id = last_id.id
    instance.unique_id = f"{instance.name}_{last_id + 1}"