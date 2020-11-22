from django.db import models
from artista.models import Artista

# Create your models here.
class Album(models.Model):
    nombre = models.CharField(max_length=100)
    artista_id = models.ForeignKey(to=Artista,on_delete=models.CASCADE)
    caratula = models.ImageField(upload_to='album')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'album_album'
