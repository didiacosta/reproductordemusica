from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# Create your views here.

def login_view(request):
	mensaje = ''
	if request.user.is_authenticated:
		# Lo redirecciono al homepage de mi aplicacion
		return redirect(reverse('usuario.home'))
	else:
		if request.method == 'POST':
			username = request.POST.get('usuario')
			password = request.POST.get('password')
			user = authenticate(username=username, password=password)

			if user:
				# el usuario existe, voy a ver si esta activo:
				if user.is_active:
					# redireccionar al homepage
					login(request, user)
					return redirect(reverse('usuario.home'))
				else:
					mensaje = 'el usuario ' + username + ' no se encuentra activo, ' + \
					'consulte con el administrador del sistema'

			else:
				# el usuario no existe
				mensaje = 'no se encontro un usuario con el nombre ' + username

	return render(request, 'usuario/login2.html', {'mensaje': mensaje})

def logout_view(request):
	logout(request)
	return redirect(reverse('usuario.login'))

def home_view(request):
	username = request.user.username
	if request.user.is_authenticated:
		return render(request,'usuario/home.html',{'username':username.capitalize()}) 
	else:
		return render(request,'usuario/login2.html',{}) 
