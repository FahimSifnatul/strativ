from django.db import models

# Create your models here.
class Countries(models.Model):
	name       = models.CharField(max_length=32)
	alpha2code = models.CharField(max_length=16)
	capital    = models.CharField(max_length=32)
	population = models.IntegerField()
	timezones  = models.CharField(max_length=16)
	flag       = models.CharField(max_length=64)
	languages  = models.CharField(max_length=256)
	borders    = models.CharField(max_length=256)