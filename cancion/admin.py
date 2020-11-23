from django.contrib import admin
from .models import Cancion

# Register your models here.
class AdminCancion(admin.ModelAdmin):
	list_display = ('id','nombre','album','archivo')
	search_fields = ('nombre',)
	list_filter = ('album',)

admin.site.register(Cancion, AdminCancion)