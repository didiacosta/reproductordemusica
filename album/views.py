from django.shortcuts import render
# Create your views here.

# framework:
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

#serializers:
from .serializers import AlbumSerializer

#models:
from .models import Album


class AlbumViewSet(viewsets.ModelViewSet):
	model = Album
	queryset = Album.objects.all()
	serializer_class = AlbumSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({'message':'','status':'success','data':serializer.data})
		except:
			return Response({
				'message':'No se encontraron datos',
				'success':'fail',
				'data':''
				},
				status=status.HTTP_404_NOT_FOUND)


	def list(self, request, *args, **kwargs):
		#import pdb; pdb.set_trace()
		try:
			queryset = super(AlbumViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)
			sin_paginacion = self.request.query_params.get('sin_paginacion', None)
			artista = self.request.query_params.get('artista', None)
			nombreArtista = self.request.query_params.get('nombreArtista', None)

			mensaje=''
			qset = (~Q(id=0))
			if dato or artista or nombreArtista:
				if dato:
					qset = qset & (Q(nombre__icontains=dato) or Q(artista_id__icontains=dato))
				if artista:
					qset = qset & (Q(artista__id=artista))
				if nombreArtista:
					qset = qset & (Q(artista__nombre__icontains=nombreArtista))



			queryset = self.model.objects.filter(qset)

			if queryset.count() == 0:
				mensaje='No se encontraron registros con los parametros de busqueda ingresados'

			if sin_paginacion is None:
				page = self.paginate_queryset(queryset)

				if page is not None:
					serializer = self.get_serializer(page,many=True)
					return self.get_paginated_response({'message':mensaje,'success':'ok',
					'data':serializer.data})
			else:
				serializer = self.get_serializer(queryset,many=True)
				return Response({'message':mensaje,'success':'ok',
					'data':serializer.data})


		except Exception as e:
			return Response({
				'message':'Se presentaron errores de comunicacion',
				'success':'fail',
				'data':''},
				status=status.HTTP_404_NOT_FOUND)

	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			try:
				serializer = AlbumSerializer(data = request.data, context ={'request':request})
				if serializer.is_valid():
					serializer.save(artista_id=request.data['artista_id'])

					return Response({'message':'El registro ha sido guardado exitosamente','success':'ok',
						'data':serializer.data},status=status.HTTP_201_CREATED)
				else:
					return Response({'message':'datos requeridos no fueron recibidos','success':'fail',
					'data':''},status=status.HTTP_400_BAD_REQUEST)

			except Exception as e:
				print(e)
				return Response({
					'message':'Se presentaron errores de comunicacion',
					'success':'fail',
					'data':''},
					status=status.HTTP_404_NOT_FOUND)


	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()				
				serializer = AlbumSerializer(instance,data=request.data,context={'request': request},partial=partial)
				if serializer.is_valid():
					serializer.save(artista_id=instance.album.id)
					return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok',
						'data':serializer.data},status=status.HTTP_201_CREATED)
				else:
					return Response({'message':'datos requeridos no fueron recibidos','success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)					
			except Exception as e:
				print(e)
				return Response({'message':'Se presentaron errores de comunicacion','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

	def destroy(self,request,*args,**kwargs):
		try:
			instance = self.get_object()
			self.perform_destroy(instance)
			return Response({'message':'El registro ha sido eliminado exitosamente','success':'ok'},status=status.HTTP_201_CREATED)			
		except Exception as e:
			#print(e)
			return Response({'message':'Se presentaron errores de comunicacion','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
