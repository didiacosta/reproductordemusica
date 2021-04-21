from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    url(r'^loginapp/$', views.loginapp_view, name='auth_user_login'),
	url(r'^login/$', views.login_view, name='usuario.login'),
	url(r'^home/$', views.home_view, name='usuario.home'),
	url(r'^logout/$', views.logout_view, name='usuario.logout'),
    url(r'^loginobtaintoken/$', obtain_auth_token, name='auth_user_login'),
]