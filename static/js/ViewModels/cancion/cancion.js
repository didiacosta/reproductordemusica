function CancionViewModel() {
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

    self.paginacion.pagina_actual.subscribe(function (pagina) {    
       self.consultar(pagina);
    });

    self.llenar_paginacion = function (data,pagina) {
        self.paginacion.pagina_actual(pagina);
        self.paginacion.total(data.count);       
        self.paginacion.cantidad_por_paginas(resultadosPorPagina);
    }

	self.consultar = function(pagina){
		if (pagina > 0) {
			 path = path_principal + '/api/cancion/?format=json';
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

}

var cancion = new CancionViewModel();
ko.applyBindings(cancion);