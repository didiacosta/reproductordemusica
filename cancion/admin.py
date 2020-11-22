from django.contrib import admin
from .models import Cancion

# Register your models here.
class AdminCancion(admin.ModelAdmin):
	list_display = ('id','nombre','album_id','caratula')
	search_fields = ('nombre',)
	list_filter = ('album_id','nombre','caratula',)

admin.site.register(Cancion, AdminCancion)