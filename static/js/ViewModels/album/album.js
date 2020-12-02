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
     self.limpiar=function(){        
		self.albumVO.id(0);
		self.albumVO.nombre('');
		self.albumVO.caratula('');
		self.albumVO.artista_id('');
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
	self.cargar = function () {
		//alert('agregando registro del album...');		
		$('#nuevoAlbum').modal('show');
		self.albumVO = {
			id: self.albumVO.id,
			nombre: self.albumVO.nombre,
			caratula: self.albumVO.caratula,
			artista_id: self.albumVO.artista_id,
		}		
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
				self.limpiar();			
			}else {
				var parametros={     
					metodo:'PUT',                
				   	callback:function(datos, estado, mensaje){
					if (estado=='ok') {
					  self.filtro("");
					  self.consultar(1);
					  $('#nuevoAlbum').modal('hide');
					  self.limpiar();
					}  

				   },//funcion para recibir la respuesta 
				   url:path_principal+'/api/album/'+self.albumVO.id()+'/',
				   parametros:self.albumVO                      
			  };

			  RequestFormData(parametros);
				self.limpiar();							
			}

		}else {
			AlbumViewModel.errores_album.showAllMessages();
		}
	}

	self.editar_album = function (obj) {
		self.llenarArtista();
		path =path_principal+'/api/album/'+obj.id+'/?format=json';
		RequestGet(function (results,count) {           		
			self.albumVO.id(results.id);
			self.albumVO.nombre(results.nombre);
			self.albumVO.caratula(results.caratula);         			
			self.albumVO.artista_id(results.artista_id);         						   			
			$('#nuevoAlbum').modal('show');
		}, path, parameter);
	}	


    self.eliminar_album = function (obj) {

		//var lista_id=[];
		//lista_id.push({id:self.albumVO.id});
		// var count=0;
		// ko.utils.arrayForEach(self.listado(), function(d) {

		// 	   if(d.eliminado()==true){
		// 		   count=1;
		// 		  lista_id.push({
		// 			   id:d.id
		// 		  })
		// 	   }
		// });

		// if(count==0){

		// 	 $.confirm({
		// 	   title:'Informativo',
		// 	   content: '<h4><i class="text-info fa fa-info-circle fa-2x"></i>Seleccione un cargo para la eliminacion.<h4>',
		// 	   cancelButton: 'Cerrar',
		// 	   confirmButton: false
		//    });

		// }else{
			var path =path_principal+'/api/album/'+obj.id+'/';
			//var parameter = { lista: lista_id};
			var parameter = {}
			RequestAnularOEliminar("Esta seguro que desea eliminar los cargos seleccionados?", path, parameter, function () {
				self.consultar(1);				
			})

	}     
   
	   
   }	

//}

var album = new AlbumViewModel();
AlbumViewModel.errores_album = ko.validation.group(album.albumVO);
ko.applyBindings(album,document.getElementById('add'));
ko.applyBindings(album,document.getElementById('actions'));
ko.applyBindings(album,document.getElementById('nuevoAlbum'));