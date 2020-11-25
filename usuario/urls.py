from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login_view, name='usuario.login'),
	url(r'^home/$', views.home_view, name='usuario.home'),
	url(r'^logout/$', views.logout_view, name='usuario.logout'),
]