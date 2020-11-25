from django.contrib import admin
from .models import Usuario
# Register your models here.

class AdminUsuario(admin.ModelAdmin):
	list_display=('id','user','foto_usuario')
	search_field=('user',)

admin.site.register(Usuario,AdminUsuario)
