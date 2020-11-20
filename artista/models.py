from django.db import models

# Create your models here.
class Artista(models.Model):
	nombre = models.CharField(max_length=100)
	nombreArtistico = models.CharField(max_length=100)

	class Meta:
		db_table = 'artista_artista'
