function ArtistaViewModel() {
	var self = this;
	self.listado = ko.observableArray([]);
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
    self.artistaVO = {
    	id: ko.observable(0),
    	nombre: ko.observable('').extend({ required: { message: ' Digite el nombre del artista.' } }),
    	nombreArtistico: ko.observable('').extend({ required: { message: ' Debe digitar el nombre artistico.' } }),    	
    }
    self.paginacion.pagina_actual.subscribe(function (pagina) {    
       self.consultar(pagina);
    });

    self.llenar_paginacion = function (data,pagina) {
        self.paginacion.pagina_actual(pagina);
        self.paginacion.total(data.count);       
        self.paginacion.cantidad_por_paginas(resultadosPorPagina);
    }
	self.limpiar=function(){        
		self.artistaVO.id(0);
		self.artistaVO.nombre('');
		self.artistaVO.nombreArtistico('');
     }
	self.consultar = function(pagina){
		if (pagina > 0) {
			 path = path_principal + '/api/artista/?format=json';
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
		//alert('agregando registro del_artista...');		
		$('#nuevoArtista').modal('show');		
	}


	self.guardar_artista = function () {
		if (ArtistaViewModel.errores_artista().length == 0) {
			if (self.artistaVO.id() == 0) {
				// voy a crear un_artista
				var parametros={
					callback:function(datos, success, mensaje){

						if (success=='ok') {
							$('#nuevoArtista').modal('hide');
							self.consultar(1);
						}else{
							 mensajeError(mensaje);
						}
					}, //funcion para recibir la respuesta 
					url:path_principal+'/api/artista/',//url api
					parametros:self.artistaVO,
					alerta:true,
					metodo: 'POST'
				};
				RequestFormData(parametros);
				self.limpiar()				
			}else {
				var parametros={     
					metodo:'PUT',                
				   	callback:function(datos, estado, mensaje){
					if (estado=='ok') {
					  self.filtro("");
					  self.consultar(1);
					  $('#nuevoArtista').modal('hide');
					  self.limpiar();
					}  

				   },//funcion para recibir la respuesta 
				   url:path_principal+'/api/artista/'+self.artistaVO.id()+'/',
				   parametros:self.artistaVO,
				   alerta:true                      
			  };

			  RequestFormData(parametros);
				self.limpiar();					
			}

		}else {
			ArtistaViewModel.errores_artista.showAllMessages();
		}
	}

	self.editar_artista = function (obj) {		
		path =path_principal+'/api/artista/'+obj.id+'/?format=json';
		RequestGet(function (results,count) {           		
			self.artistaVO.id(results.id);
			self.artistaVO.nombre(results.nombre);
			self.artistaVO.nombreArtistico(results.nombreArtistico);         						      						   			
			$('#nuevoArtista').modal('show');
		}, path, parameter);		
	}

}

var artista = new ArtistaViewModel();
ArtistaViewModel.errores_artista = ko.validation.group(artista.artistaVO);
ko.applyBindings(artista,document.getElementById('add'));
ko.applyBindings(artista,document.getElementById('actions'));
ko.applyBindings(artista,document.getElementById('nuevoArtista'));
