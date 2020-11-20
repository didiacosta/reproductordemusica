from django.db import models

# Create your models here.
class Artista(models.Model):
	nombre = models.CharField(max_length=100)
	nombreArtistico = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'artista_artista'
