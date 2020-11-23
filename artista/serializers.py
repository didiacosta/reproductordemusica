# modelos:
from .models import Artista

#framework:
from rest_framework import serializers

class ArtistaSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Artista
		fields=('id','nombre','nombreArtistico')