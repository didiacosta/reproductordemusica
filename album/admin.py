from django.contrib import admin
from .models import Album

# Register your models here.
class AdminAlbum(admin.ModelAdmin):
    list_display = ('id','nombre','artista_id','caratula')
    search_fields = ('nombre',)
    list_filter = ('artista_id','nombre','caratula',)    

admin.site.register(Album, AdminAlbum)