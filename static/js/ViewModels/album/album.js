function AlbumViewModel() {
	var self = this;
	self.listado = ko.observableArray([]);
	self.listadoDeArtistas = ko.observableArray([]);
	self.mensaje = ko.observable('');

	 self.paginacion = {
        pagina_actual: ko.observable(1),
        total: ko.observable(0),
        maxPaginas: ko.observable(5),
        directiones: ko.observable(true),
        limite: ko.observable(true),
        cantidad_por_paginas: ko.observable(0),
        text: {
            first: ko.observable('Inicio'),
            last: ko.observable('Fin'),
            back: ko.observable('«'),
            forward: ko.observable('»')
        }
    }

    self.paginacion.pagina_actual.subscribe(function (pagina) {    
       self.consultar(pagina);
    });

    self.llenar_paginacion = function (data,pagina) {
        self.paginacion.pagina_actual(pagina);
        self.paginacion.total(data.count);       
        self.paginacion.cantidad_por_paginas(resultadosPorPagina);
    }

    self.albumVO = {
    	id: ko.observable(0),
    	nombre: ko.observable('').extend({ required: { message: ' Digite el nombre del album.' } }),
    	caratula: ko.observable('').extend({ required: { message: ' Debe cargar la imagen de la caratula.' } }),
    	artista_id: ko.observable(0).extend({ required: { message: ' Seleccione el artista.' } })
    }

	self.consultar = function(pagina){
		if (pagina > 0) {
			 path = path_principal + '/api/album/?format=json';
			 if (pagina == 1){
				parameter = {
					dato: $('#txtBuscar').val()
				}
			 }else{
				parameter = {
				 	dato: $('#txtBuscar').val(),
				 	offset: pagina
			 	}

			 }
			 RequestGet(function (datos, success, mensage) {
			 	if (success == 'ok' && datos.data!=null && datos.data.length > 0) {
			 		self.mensaje('');
			 		self.listado(agregarOpcionesObservable(datos.data));
			 	} else {
			 		self.listado([]);
			 		self.mensaje(mensajeNoFound);
			 		cerrarLoading()
			 	}
			 	self.llenar_paginacion(datos,pagina);
			 	cerrarLoading();

			 },path, parameter,undefined, false);
		}
	}

	self.consulta_enter = function(d,e){
		if (e.which == 13) {
            self.consultar(1);
		}
		return true;
	}
	self.consultar_boton = function(){
		self.consultar(1);
		return true;
	}
	self.agregar = function () {
		//alert('agregando registro del album...');
		$('#nuevoAlbum').modal('show');
		self.llenarArtista();
	}

	self.llenarArtista = function () {
		path = path_principal + '/api/artista/?format=json';
		parameter = {
		 	sin_paginacion: 1
	 	}
		 RequestGet(function (datos, success, mensage) {
		 	if (success == 'ok' && datos!=null && datos.length > 0) {	
		 		self.listadoDeArtistas(agregarOpcionesObservable(datos));
		 	} else {
		 		self.listadoDeArtistas([]);
		 	}
		 	cerrarLoading();
		 },path, parameter,undefined, false);
		 
	}

	self.guardar_album = function () {
		if (AlbumViewModel.errores_album().length == 0) {
			if (self.albumVO.id() == 0) {
				// voy a crear un album
				var parametros={
					callback:function(datos, success, mensaje){

						if (success=='ok') {
							$('#nuevoAlbum').modal('hide');
							self.consultar(1);
						}else{
							 mensajeError(mensaje);
						}
					}, //funcion para recibir la respuesta 
					url:path_principal+'/api/album/',//url api
					parametros:self.albumVO,
					alerta:true,
					metodo: 'POST'
				};
				RequestFormData(parametros);
			}else {
				// voy a modificar un album
			}

		}else {
			AlbumViewModel.errores_album.showAllMessages();
		}
	}

}

var album = new AlbumViewModel();
AlbumViewModel.errores_album = ko.validation.group(album.albumVO);
ko.applyBindings(album);