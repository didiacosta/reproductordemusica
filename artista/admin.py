from django.contrib import admin
from .models import Artista
# Register your models here.

class AdminArtista(admin.ModelAdmin):
	list_display = ('id','nombre','nombreArtistico')
	search_fields = ('nombreArtistico',)


admin.site.register(Artista, AdminArtista)
