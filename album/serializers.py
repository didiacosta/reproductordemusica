# modelos:
from .models import Album, Artista

#serializers
from artista.serializers import ArtistaSerializer

#framework:
from rest_framework import serializers

class AlbumSerializer(serializers.HyperlinkedModelSerializer):
	artista_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Artista.objects.all())
	artista = ArtistaSerializer(read_only=True)

	class Meta:
		model = Album
		fields=('id','nombre','artista','artista_id','caratula')