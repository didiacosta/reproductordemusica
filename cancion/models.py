from django.db import models
from album.models import Album

# Create your models here.
class Cancion(models.Model):
    nombre = models.CharField(max_length=100)
    album_id = models.ForeignKey(to=Album,on_delete=models.CASCADE)
    caratula = models.FileField(upload_to='cancion')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'cancion_cancion'