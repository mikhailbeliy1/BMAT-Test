from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class MusicalWork(models.Model):
    title = models.CharField(max_length=50, unique=True)
    contributors = ArrayField(
        models.CharField(max_length=30),
        size=8,
    )
    iswc = models.CharField(max_length=50, unique=True)
