from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
# Create your views here.

def loginout_view(request):
	logout(request)
	return Response({
		'message': mensaje, 'success':'ok',
			'data': {
				'autenticado': 0	
			}
		})

@api_view(['POST'])
def loginapp_view(request):
	mensaje = ''
	# if request.user.is_authenticated:
	# 	return Response({
	# 		'message': mensaje, 'success':'ok',
	# 			'data': {
	# 				'autenticado': 1,
	# 				'username' : request.user.username	
	# 			}
	# 		})

	# else:
	
	autenticado = 0
	username=''
	success = 'error'
	if request.method == 'POST':
		data = request.body.decode('utf8').replace("'",'"')
		data = json.loads(data)

		#import pdb; pdb.set_trace()
		username = data['username']
		password = data['password']

		user = authenticate(username=username, password=password)	
		if user:
			# el usuario existe, voy a ver si esta activo:
			if user.is_active:
				# redireccionar al homepage
				login(request, user)
				autenticado = 1
				#import pdb; pdb.set_trace()
				username = user.username
				success = 'ok'
			else:
				mensaje = 'el usuario ' + username + ' no se encuentra activo, ' + \
				'consulte con el administrador del sistema'
		else:
			# el usuario no existe
			mensaje = 'Error, por favor verifique su usuario y contraseña'
		return Response({
		'message': mensaje, 'success':success,
			'data': {
				'autenticado': autenticado,
				'username' : username	
			}
		})

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
