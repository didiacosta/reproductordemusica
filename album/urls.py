from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^home/$', views.home_view, name='album.home'),
	url(r'^eliminar_album/$', views.eliminar_album, name='album.eliminar_album'),
]