from django.db import models

# Create your models here.
class Parking(models.Model):
    total_spaces = models.IntegerField()
    available_spaces = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)