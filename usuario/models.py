from django.db import models
from django.conf import settings
from django.utils.html import format_html

# Create your models here.
class Usuario(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	foto = models.ImageField(upload_to='usuario',blank=True, null=True)

	def __str__(self):
		return str(self.user.username) or u''

	def foto_usuario(self):
		if self.foto:
			return format_html('<img src="{}" width="100" height="100"/>'.format(str(self.foto.url)))
		else:
			return None

	foto_usuario.allow_tags = True
