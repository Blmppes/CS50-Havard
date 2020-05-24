from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100000)
    summary = models.TextField()
    feature = models.BooleanField()
