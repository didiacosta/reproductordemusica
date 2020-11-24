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

			qset = (~Q(id=0))
			if dato:
				qset = qset & (Q(nombre__icontains=dato) or Q(artista_id__icontains=dato))

			queryset = self.model.objects.filter(qset)

			if sin_paginacion is None:
				page = self.paginate_queryset(queryset)

				if page is not None:
					serializer = self.get_serializer(page,many=True)
					return self.get_paginated_response({'message':'','success':'ok',
					'data':serializer.data})
			else:
				serializer = self.get_serializer(queryset,many=True)
				return Response({'message':'','success':'ok',
					'data':serializer.data})


		except Exception as e:
			print(e)
			return Response({
				'message':'Se presentaron errores de comunicacion',
				'success':'fail',
				'data':''},
				status=status.HTTP_404_NOT_FOUND)

	def create(self, request, *args, **kwargs):
		pass

	def update(self,request,*args,**kwargs):
		pass

	def destroy(self,request,*args,**kwargs):
		pass
