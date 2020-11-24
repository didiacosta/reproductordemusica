# modelos:
from .models import Album, Cancion

#serializers
from album.serializers import AlbumSerializer

#framework:
from rest_framework import serializers

class CancionSerializer(serializers.HyperlinkedModelSerializer):
	album_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Album.objects.all())
	album = AlbumSerializer(read_only=True)

	class Meta:
		model = Cancion
		fields=('id','nombre','album','album_id','archivo')