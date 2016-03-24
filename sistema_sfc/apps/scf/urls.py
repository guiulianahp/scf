from django.conf.urls import patterns, url

urlpatterns = patterns('sistema_sfc.apps.scf.views',
	url(r'^add/cliente/$','add_cliente_view',name="vista_agregar_cliente"),
	url(r'^add/cliente/(?P<id_prospecto>.*)/$','add_prospecto_to_cliente_view',name="vista_agregar_prospecto_a_cliente"),
	url(r'^add/producto/$','add_producto_view',name="vista_agregar_producto"),
	url(r'^add/prospecto/$','add_prospecto_view',name="vista_agregar_prospecto"),
	url(r'^add/cotizacion/$','add_cotizacion_view',name="vista_agregar_cotizacion"),
	url(r'^add/factura/$','add_factura_view',name="vista_agregar_factura"),
	url(r'^add/observacion/$','add_observacion_view',name="vista_agregar_observacion"),
	url(r'^edit/cliente/(?P<id_cliente>.*)/$','edit_cliente_view',name="vista_editar_cliente"),
	url(r'^edit/producto/(?P<id_producto>.*)/$','edit_producto_view',name="vista_editar_producto"),
	url(r'^edit/prospecto/(?P<id_prospecto>.*)/$','edit_prospecto_view',name="vista_editar_prospecto"),
	url(r'^edit/cotizacion/(?P<id_cotizacion>.*)/$','edit_cotizacion_view',name="vista_editar_cotizacion"),
	url(r'^edit/observacion/(?P<id_observacion>.*)/$','edit_observacion_view',name="vista_editar_observacion"),
	url(r'^cotizacion/(?P<id_cotizacion>.*)/$','factura_preview',name="vista_factura_preview"),
	url(r'^save/cotizacion/$','save_cotizacion',name="vista_guardar_cotizacion"),
	url(r'^pdf/cotizacion/(?P<id_cotizacion>.*)/$','generate_pdf_cotizacion',name="vista_generar_pdf_cotizacion"),
	url(r'^ver/cotizacion/(?P<id_cotizacion>.*)/$','ver_cotizacion_view',name="vista_ver_cotizacion"),
	url(r'^pdf/factura/(?P<id_factura>.*)/$','generate_pdf_factura')
	)
