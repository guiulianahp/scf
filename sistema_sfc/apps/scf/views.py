# -*- encoding: utf-8 -*-

import cgi
import json
import math
from io import BytesIO
from datetime import date
import cStringIO as StringIO
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse
from django.views.generic import ListView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.datastructures import MultiValueDictKeyError

from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import flowables
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4,letter, inch, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Image, Table, TableStyle,KeepTogether, Paragraph, Spacer
from reportlab.lib.colors import (black, green, white, yellow)

from sistema_sfc.apps.scf.forms import addClienteForm, addProductoForm, addProspectoForm, addCotizacion, addObservacionForm
from sistema_sfc.apps.scf.models import Cliente, Producto, Prospecto, Cotizacion, Producto_has_cotizacion, Factura, Observacion, Observacion_por_defecto

global_limit = 6

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(self)
        self._startPage()

    def draw_message_footer(self):
        self.setFont("Helvetica", 10)
        message = 'Av. Paseo Caroní, Casa Nº10, Urbanización Morichal Nº1, Puerto Ordaz - Edo. Bolívar    '

        self.drawRightString(177*mm, 30*mm,message)


    def save(self):
        
        for state in self._saved_page_states:
            #self.draw_page_number(num_pages)

            if state == self._saved_page_states[-1]:
            	print state
            	self.draw_message_footer()
            	canvas.Canvas.showPage(self)
            else:
                ## If it's not the last page, explicitly pass over it.  Just being thorough here.
                pass
            #self.draw_message_footer()
            
        canvas.Canvas.save(self)
        
    
    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm,
            "Page %d of %d" % (self._pageNumber, page_count))

def add_cliente_view(request):
	if request.method == "POST":
		form = addClienteForm(request.POST)
		info = "Inicializando"
		if form.is_valid():
			rif 		= form.cleaned_data['rif']
			nombre 		= form.cleaned_data['nombre']
			telefono 	= form.cleaned_data['telefono']
			correo 		= form.cleaned_data['correo']
			direccion 	= form.cleaned_data['direccion']

			client 				= Cliente()
			client.rif 			= rif
			client.nombre 		= nombre
			client.telefono 	= telefono
			client.correo 		= correo
			client.direccion 	= direccion
			client.save()
			info = "Datos guardados satisfactoriamente"
			status = "True"
		else:
			info = "Informacion con datos incorrectos"
			status = "False"
		form = addClienteForm()
		ctx  = {'form': form, 'informacion': info, 'status':status}
		return render_to_response('scf/addCliente.html',ctx,context_instance = RequestContext(request))


	else: #GET
		form = addClienteForm()
		ctx  = {'form':form}
		return render_to_response('scf/addCliente.html',ctx,context_instance = RequestContext(request))

def add_prospecto_to_cliente_view(request, id_prospecto):
	if request.method == "POST":
		form = addClienteForm(request.POST)
		info = "Inicializando"
		if form.is_valid():
			rif 		= form.cleaned_data['rif']
			nombre 		= form.cleaned_data['nombre']
			telefono 	= form.cleaned_data['telefono']
			correo 		= form.cleaned_data['correo']
			direccion 	= form.cleaned_data['direccion']

			client 				= Cliente()
			client.rif 			= rif
			client.nombre 		= nombre
			client.telefono 	= telefono
			client.correo 		= correo
			client.direccion 	= direccion
			client.save()

			p = Prospecto.objects.get(id=id_prospecto)
			p.delete() # Elinamos objeto de la base de datos
			
			info = "Datos guardados satisfactoriamente"
		else:
			info = "Informacion con datos incorrectos"
		form = addClienteForm()
		
		ctx  = {'form': form, 'informacion': info}
		return render_to_response('scf/addCliente.html',ctx,context_instance = RequestContext(request))

	else: #GET
		prospecto = Prospecto.objects.get(id = id_prospecto)
		form = addClienteForm()
		form.fields["nombre"].initial = prospecto.nombre
		form.fields["telefono"].initial = prospecto.telefono
		form.fields["correo"].initial = prospecto.correo
		ctx  = {'form':form}
		return render_to_response('scf/addCliente.html',ctx,context_instance = RequestContext(request))

def add_producto_view(request):
	if request.method == "POST":
		form = addProductoForm(request.POST)
		info = "Inicializando"
		if form.is_valid():
			nombre 		= form.cleaned_data['nombre']
			descripcion	= form.cleaned_data['descripcion']
			precio_tp	= form.cleaned_data['precio_talla_pequena']
			
			checkbox = request.POST.get('talla_grande', False)
			if checkbox:
				precio_tg = (precio_tp*0.10)+precio_tp
			else:
				precio_tg = 0
			
			producto				= Producto()
			producto.nombre 		= nombre
			producto.descripcion 	= descripcion
			producto.precio_tp 		= precio_tp
			producto.precio_tg 		= precio_tg
			producto.save()
			info = "Datos guardados satisfactoriamente"

			form = addProductoForm()
			ctx  = {'form': form, 'informacion': info}
			return render_to_response('scf/addProducto.html',ctx,context_instance = RequestContext(request))
		
		else:
			info = "Informacion con datos incorrectos"
			ctx  = {'form': form, 'informacion': info}
			return render_to_response('scf/addProducto.html',ctx,context_instance=RequestContext(request))


	else: #GET
		form = addProductoForm()
		ctx  = {'form':form}
		return render_to_response('scf/addProducto.html',ctx,context_instance = RequestContext(request))

def add_prospecto_view(request):
	if request.method == "POST":
		form = addProspectoForm(request.POST)
		info = "Inicializando"
		if form.is_valid():
			nombre 		= form.cleaned_data['nombre']
			telefono 	= form.cleaned_data['telefono']
			correo 		= form.cleaned_data['correo']
			
			prospecto			= Prospecto()
			prospecto.nombre 	= nombre
			prospecto.telefono 	= telefono
			prospecto.correo 	= correo
			prospecto.save()
			info = "Datos guardados satisfactoriamente"
		else:
			info = "Informacion con datos incorrectos"
		form = addProspectoForm()
		ctx  = {'form': form, 'informacion': info}
		return render_to_response('scf/addProspecto.html',ctx,context_instance = RequestContext(request))


	else: #GET
		form = addProspectoForm()
		ctx  = {'form':form}
		return render_to_response('scf/addProspecto.html',ctx,context_instance = RequestContext(request))

@ensure_csrf_cookie
def add_cotizacion_view(request):
	today 		  = date.today()
	clients 	  = Cliente.objects.order_by('id')	
	list_product  = Producto.objects.order_by('id')
	observaciones = Observacion_por_defecto.objects.order_by('id')
	return render_to_response('scf/addCotizacion.html', {'date':today, 'clients':clients, 'list_product' : list_product, 'observaciones': observaciones}, context_instance=RequestContext(request))

@ensure_csrf_cookie
def add_factura_view(request):
	if request.method == "GET":
		resultado = []
		#cotizaciones = Cotizacion.objects.order_by('id')
		cotizaciones = Cotizacion.objects.filter(estado = 0).extra(select={'estado':0})
		
		clientes = Cliente.objects.order_by('id')
		objeto = {'id':'', 'cliente':'','fecha':''}
		for cotizacion in cotizaciones:
			id_cliente = cotizacion.cliente_identificacion_id
			for cliente in clientes:
				if id_cliente == cliente.id:
					objeto['id'] = cotizacion.id
					objeto['fecha'] = cotizacion.fecha
					objeto['cliente'] = cliente.nombre
					resultado.append(objeto)
					objeto = {'id':'', 'cliente':'','fecha':''}

		return render_to_response('scf/addFactura.html', {'cotizacion_view' : resultado}, context_instance=RequestContext(request))
	
	if request.method == "POST" and request.is_ajax():

		date  = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
		cotizacion_id = request.POST['id_cotizacion']
		factura_id = request.POST['id_factura']
		
		
		try:
			factura = Factura.objects.get(num_factura = factura_id)
			boolean = True
		except Factura.DoesNotExist:
			boolean = False

		if boolean:
			response = HttpResponse('Nro de factura ya existente', status=400)
			response['Content-Length'] = len(response.content)
			return response

		try:
			last_created = Factura.objects.all().last()

			#OBTENER LOS PRODUCTOS DE LA COTIZACION
			productos_cotizacion = Producto_has_cotizacion.objects.filter(cotizacion_id_cotizacion_id = last_created.cotizacion_id_cotizacion_id).extra(select={'cotizacion_id_cotizacion_id':last_created.cotizacion_id_cotizacion_id})
			cantidad_total = len(productos_cotizacion) / float(global_limit)

			num_factura = int(factura_id)
			

			if not cantidad_total.is_integer(): 
				cantidad_total = int(cantidad_total) + 1
			else:
				cantidad_total = int(cantidad_total)

			print num_factura
			print cantidad_total
			print len(productos_cotizacion)
			print global_limit
			print cotizacion_id

			if num_factura <= (last_created.num_factura + (cantidad_total -1)):
				response = HttpResponse('Nro de factura ya existente', status=400)
				response['Content-Length'] = len(response.content)
				return response

			if last_created.num_factura > int(factura_id):
				response = HttpResponse('El Nro de Factura no es correcto (Nro de Factura menor)', status=401)
				response['Content-Length'] = len(response.content)
				return response
		except Exception as e:
			print e
			pass

		if not boolean:
			cotizacion = Cotizacion.objects.get(id = cotizacion_id)
			cotizacion.estado = 1
			cotizacion.save()

			factura = Factura()
			factura.num_factura = factura_id
			factura.fecha = date
			factura.cotizacion_id_cotizacion_id = cotizacion_id
			factura.save() 

			return HttpResponseRedirect('/facturacion/')
		#return redirect(reverse("/facturacion/"), {"alert":'true'})
		#return HttpResponseRedirect('/facturacion/')

def add_observacion_view(request):
	if request.method == "POST":
		form = addObservacionForm(request.POST)
		info = "Inicializando"
		if form.is_valid():
			descripcion	= form.cleaned_data['descripcion']

			observacion		  		= Observacion_por_defecto()
			observacion.descripcion = descripcion
			observacion.save()
			info = "Datos guardados satisfactoriamente"
		else:
			info = "Informacion con datos incorrectos"
		form = addObservacionForm()
		ctx  = {'form': form, 'informacion': info}
		return render_to_response('scf/addObservacion.html',ctx,context_instance = RequestContext(request))


	else: #GET
		form = addObservacionForm()
		ctx  = {'form':form}
		return render_to_response('scf/addObservacion.html',ctx,context_instance = RequestContext(request))
		
def edit_cliente_view(request,id_cliente):
	cliente = Cliente.objects.get(id=id_cliente)
	if request.method == "POST":
		form = addClienteForm(request.POST,request.FILES)
		if form.is_valid():
			rif 		= form.cleaned_data['rif']
			nombre 		= form.cleaned_data['nombre']
			telefono 	= form.cleaned_data['telefono']
			correo 		= form.cleaned_data['correo']
			direccion 	= form.cleaned_data['direccion']

			cliente.rif 		= rif
			cliente.nombre 		= nombre
			cliente.telefono 	= telefono
			cliente.correo 		= correo
			cliente.direccion 	= direccion
			cliente.save()
			return HttpResponseRedirect('/cliente/')
	if request.method == "GET":
		form = addClienteForm(initial = {
			'rif' : cliente.rif,
			'nombre' : cliente.nombre,
			'telefono' : cliente.telefono,
			'correo' : cliente.correo,
			'direccion' : cliente.direccion,
			})
	ctx = {'form': form, 'cliente':cliente}
	return render_to_response('scf/editCliente.html',ctx, context_instance = RequestContext(request))

def edit_producto_view(request,id_producto):
	producto = Producto.objects.get(id=id_producto)
	
	if request.method == "POST":
		form = addProductoForm(request.POST,request.FILES)

		if form.is_valid():
			nombre 		= form.cleaned_data['nombre']
			descripcion	= form.cleaned_data['descripcion']
			precio_tp	= form.cleaned_data['precio_talla_pequena']

			checkbox = request.POST.get('talla_grande', False)
			if checkbox:
				precio_tg = (precio_tp*0.10)+precio_tp
			else:
				precio_tg = 0			

			producto.nombre 		= nombre
			producto.descripcion 	= descripcion
			producto.precio_tp 		= precio_tp
			producto.precio_tg 		= precio_tg
			producto.save()
	
			return HttpResponseRedirect('/producto/')
	if request.method == "GET":
		form = addProductoForm(initial = {
			'nombre' : producto.nombre,
			'descripcion' : producto.descripcion,
			'precio_talla_pequena' : producto.precio_tp
			})
		
	ctx = {'form': form, 'producto':producto}
	return render_to_response('scf/editProducto.html',ctx, context_instance = RequestContext(request))

def edit_prospecto_view(request,id_prospecto):
	prospecto = Prospecto.objects.get(id=id_prospecto)
	if request.method == "POST":
		form = addProspectoForm(request.POST,request.FILES)
		if form.is_valid():
			nombre 		= form.cleaned_data['nombre']
			telefono 	= form.cleaned_data['telefono']
			correo 		= form.cleaned_data['correo']
			
			prospecto.nombre 	= nombre
			prospecto.telefono 	= telefono
			prospecto.correo 	= correo
			prospecto.save()
			return HttpResponseRedirect('/prospecto/')
	if request.method == "GET":
		form = addProspectoForm(initial = {
			'nombre' : prospecto.nombre,
			'telefono' : prospecto.telefono,
			'correo' : prospecto.correo,
			})
	ctx = {'form': form, 'prospecto':prospecto}
	return render_to_response('scf/editProspecto.html',ctx, context_instance = RequestContext(request))

def edit_cotizacion_view(request, id_cotizacion):
	values = []

	if request.method =="POST" and request.is_ajax():
		
		try:
			rifClient 			= request.POST['rifClient']
			
			array_productos 	= request.POST['value']
			value_productos  	= json.loads(array_productos)

			array_observaciones = request.POST['observaciones']
			value_observaciones = json.loads(array_observaciones)

			id_cliente = Cliente.objects.get(rif = rifClient)
			cotizacion = Cotizacion.objects.get(id = id_cotizacion)

			cotizacion.cliente_identificacion_id = id_cliente
			cotizacion.save()

			cotizacion_productos     = Producto_has_cotizacion.objects.filter(cotizacion_id_cotizacion_id = id_cotizacion).extra(select={'cotizacion_id_cotizacion_id':id_cotizacion}).delete()
			cotizacion_observaciones = Observacion.objects.filter(cotizacion_id = id_cotizacion).extra(select={'cotizacion_id':id_cotizacion}).delete()
			
		except MultiValueDictKeyError:
			value_productos = []
		
		
		for item in value_productos:
			id_producto = item['id']
			cantidad 	= item['cantidad']
			ganancia 	= item['ganancia']
			precio 		= item['precio']
			talla 		= item['talla']
			
			producto_cotizacion 							= Producto_has_cotizacion()
			producto_cotizacion.cantidad 					= cantidad
			producto_cotizacion.ganancia 					= ganancia
			producto_cotizacion.cotizacion_id_cotizacion_id = id_cotizacion
			producto_cotizacion.producto_id_producto_id 	= id_producto
			producto_cotizacion.precio 						= precio
			producto_cotizacion.talla 						= talla


			producto_cotizacion.save()

		for item in value_observaciones:
			observacion_cotizacion 					= Observacion()
			observacion_cotizacion.cotizacion_id 	= id_cotizacion
			observacion_cotizacion.descripcion 		= item['observacion']

			observacion_cotizacion.save()

		return HttpResponseRedirect('/cotizacion/')

	if request.method == "GET":
		count = 1
		total = 0
		table_productos = []
		table_observacion = []

		cotizacion 			 = Cotizacion.objects.get(id=id_cotizacion);
		cliente_informacion  = Cliente.objects.get(id=cotizacion.cliente_identificacion_id)
		cotizacion_productos = Producto_has_cotizacion.objects.filter(cotizacion_id_cotizacion_id = id_cotizacion).extra(select={'cotizacion_id_cotizacion_id':id_cotizacion})
		
		clientes  = Cliente.objects.order_by('id')
		productos = Producto.objects.order_by('id')
		

		observaciones 			 = Observacion_por_defecto.objects.order_by('id')
		cotizacion_observaciones = Observacion.objects.filter(cotizacion_id = id_cotizacion).extra(select={'cotizacion_id':id_cotizacion})
		
		
		objecto_productos     = {'id':'','descripcion':'','talla':'', 'cantidad':'','ganancia':'','precio_unitario':'','precio_talla_xl':'', 'precio_total':''}
		objecto_observaciones = {'id':'','observacion':''}
		
		for item in cotizacion_productos:
			producto = Producto.objects.get(id = item.producto_id_producto_id)
			objecto_productos['id'] 			 = item.producto_id_producto_id
			objecto_productos['talla'] 			 = item.talla
			objecto_productos['cantidad'] 		 = item.cantidad
			objecto_productos['ganancia']		 = item.ganancia
			objecto_productos['descripcion'] 	 = producto.descripcion
			objecto_productos['precio_total'] 	 = (item.precio * item.cantidad)*(1+(item.ganancia / 100))
			objecto_productos['precio_unitario'] = item.precio
			objecto_productos['precio_talla_xl'] = item.precio * 1.1

			total += (item.precio * item.cantidad) * (1 + (item.ganancia/100));
			table_productos.append(objecto_productos)
			objecto_productos = {'id':'','descripcion':'','talla':'', 'cantidad':'','ganancia':'','precio_unitario':'', 'precio_talla_xl':'', 'precio_total':''}
		
		for item in cotizacion_observaciones:
			objecto_observaciones['id'] 		 = count
			objecto_observaciones['observacion'] = item.descripcion

			table_observacion.append(objecto_observaciones)
			objecto_observaciones = {'id':'','observacion':''}
			count += 1
		total = float(total)
		
		ctx = {'num_observaciones': len(table_observacion),'tabla_observaciones':table_observacion, 'observaciones':observaciones, 'table':table_productos, 'cliente':cliente_informacion, 'cotizacion':cotizacion, 'list_clients':clientes, 'list_product':productos, 'total':total}
		
		return render_to_response('scf/editCotizacion.html', ctx, context_instance = RequestContext(request))

def edit_observacion_view(request,id_observacion):
	observacion = Observacion_por_defecto.objects.get(id=id_observacion)

	if request.method == "POST":
		form = addObservacionForm(request.POST,request.FILES)
		if form.is_valid():
			descripcion = form.cleaned_data['descripcion']
			
			observacion.descripcion = descripcion
			observacion.save()
			return HttpResponseRedirect('/observacion/')
	if request.method == "GET":
		form = addObservacionForm(initial = {
			'descripcion' : observacion.descripcion
			})
	ctx = {'form': form, 'informacion':'good', 'observacion':observacion}
	return render_to_response('scf/editObservacion.html',ctx, context_instance = RequestContext(request))


def ver_cotizacion_view(request,id_cotizacion):

	return render_to_response('scf/verCotizacion.html', {'id_cotizacion' : id_cotizacion}, context_instance=RequestContext(request))
	
@ensure_csrf_cookie
def save_cotizacion(request):
    if request.method == "POST" and request.is_ajax():
    	#HORA SERVIDOR
    	date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    	
    	#RIF CLIENTE
    	rifClient = request.POST['rifClient']

    	#OBTENER ID CLIENTE
    	clients = Cliente.objects.get(rif=rifClient)


    	#CREAR COTIZACION
    	cotizacion 			= Cotizacion()
    	cotizacion.fecha 	= date
    	cotizacion.cliente_identificacion_id = clients.id
    	cotizacion.save()

    	#OBTENER VALORES DE COTIZACION
    	array_productos  = request.POST['value']
        values_productos = json.loads(array_productos)
        
        for item in values_productos:
        	talla  		= item['talla']
        	precio  	= item['precio']
        	ganancia    = item['ganancia']
        	cantidad    = item['cantidad']
        	id_producto = item['id']
        	

        	#GUARDAR PRODUCTOS-COTIZACION
        	producto_cotizacion = Producto_has_cotizacion()

        	producto_cotizacion.talla 		= talla
        	producto_cotizacion.precio 		= precio
        	producto_cotizacion.cantidad 	= cantidad
        	producto_cotizacion.ganancia 	= ganancia
        	producto_cotizacion.producto_id_producto_id 	= id_producto
        	producto_cotizacion.cotizacion_id_cotizacion_id = cotizacion.id 
        	
        	producto_cotizacion.save()

    	#OBTENER VALORES DE OBSERVACION
    	array_observaciones = request.POST['observaciones']
        value_observaciones = json.loads(array_observaciones)
        
        for item in value_observaciones:
        	
        	#GUARDAR OBSERVACIONES-COTIZACION
        	observacion = Observacion()

        	observacion.cotizacion_id = cotizacion.id 
        	observacion.descripcion   = item['observacion']
        	observacion.save()

        return HttpResponseRedirect('/cotizacion/')
    else:
    	return render_to_response('home/cotizacion.html',context_instance = RequestContext(request))

def factura_preview(request,id_cotizacion):
	table = []
	data = {}
		
	if request.method == "GET" and request.is_ajax():
		cotizacion_productos = Producto_has_cotizacion.objects.filter(cotizacion_id_cotizacion_id = id_cotizacion).extra(select={'cotizacion_id_cotizacion_id':id_cotizacion})
		total = 0
		cotizacion = Cotizacion.objects.get(id=id_cotizacion);
		cliente_informacion = Cliente.objects.get(id=cotizacion.cliente_identificacion_id)
		productos = Producto.objects.order_by('id')
		clientes = Cliente.objects.order_by('id')
		objecto = {'id':'','descripcion':'','talla':'', 'cantidad':'','ganancia':'','precio_unitario':'','precio_talla_xl':'', 'precio_total':''}

		for item in cotizacion_productos:
			producto = Producto.objects.get(id= item.producto_id_producto_id)
			objecto['id'] = item.producto_id_producto_id
			objecto['talla'] = item.talla
			objecto['cantidad'] = item.cantidad
			objecto['ganancia']=int(item.ganancia)
			objecto['precio_unitario'] = item.precio
			objecto['precio_talla_xl'] = item.precio * 1.1
			objecto['descripcion'] = producto.descripcion
			objecto['talla'] = item.talla
			objecto['precio_total'] = (item.precio * item.cantidad)*(1+(item.ganancia / 100))
			total += (item.precio * item.cantidad) * (1 + (int(item.ganancia)/100));
			table.append(objecto)
			objecto = {'id':'','descripcion':'','talla':'', 'cantidad':'','ganancia':'','precio_unitario':'', 'precio_talla_xl':'', 'precio_total':''}
		
		cliente = {'id': cliente_informacion.id, 'nombre':cliente_informacion.nombre, 'rif': cliente_informacion.rif, 'telefono':cliente_informacion.telefono, 'correo':cliente_informacion.correo,'direccion':cliente_informacion.direccion}
		
		data = {"tabla":table,"total":total,"cliente":cliente}
        return HttpResponse(json.dumps(data),content_type='application/json')

def generate_pdf_factura(request, id_factura):

	#OBTENER FACTURA
	factura = Factura.objects.get(id = id_factura)

	#OBTENER TODAS LAS FACTURAS DE LA COTIZACION
	factura_cotizacion = Factura.objects.filter(cotizacion_id_cotizacion_id = factura.cotizacion_id_cotizacion_id).extra(select={'cotizacion_id_cotizacion_id':factura.cotizacion_id_cotizacion_id})

	#OBTENER COTIZACION DE LA FACTURA
	cotizacion = Cotizacion.objects.get(id = factura.cotizacion_id_cotizacion_id)

	#OBTENER TODOS LOS PRODUCTOS PARA MOSTRAR SU DESCRIPCION
	productos = Producto.objects.order_by('id')

	#OBTENER LOS RESPECTIVOS PRODUCTOS DE LA COTIZACION
	productos_cotizacion = Producto_has_cotizacion.objects.filter(cotizacion_id_cotizacion_id = cotizacion.id).extra(select={'cotizacion_id_cotizacion_id':cotizacion.id})

	#OBTENER EL CLIENTE DE LA FACTURA
	cliente = Cliente.objects.get(id=cotizacion.cliente_identificacion_id)

	count = 0
	cantidad_total = float(len(productos_cotizacion)) / float(global_limit)
	cantidad_total = math.ceil(cantidad_total)

	# VARIABLES PARA EL ARRAY DE PRODUCTOS DE LA COTIZACION
	total = 0
	total_productos = []
	objeto = {"cantidad":0, "descripcion":0, "talla":0, "precio_unitario":0, "precio_total":0, "ganancia":0}

	# OBTENER TODOS LOS PRODUCTOS DE LA COTIZACION
	for item in productos_cotizacion:
		for producto in productos:
			if producto.id == item.producto_id_producto_id:
				objeto['descripcion'] = producto.descripcion
				break
		objeto['cantidad'] = item.cantidad
		objeto['talla'] = item.talla
		objeto['precio_unitario'] = item.precio
		objeto['precio_total'] = (item.precio * item.cantidad)*(1+(item.ganancia / 100))
		objeto['ganancia'] = item.ganancia
		total_productos.append(objeto)
		total += (item.precio * item.cantidad)*(1+(item.ganancia / 100))
		objeto = {"cantidad":0, "descripcion":0, "talla":0, "precio_unitario":0, "precio_total":0, "ganancia":0}	

	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="FACTURA '+ str(factura.num_factura)+' '+cliente.nombre+'.pdf"'

	# Create the PDF object, using the response object as its "file."
	p = canvas.Canvas(response)

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	
	puntero_producto = 0
	
	while count<cantidad_total:
		
		print count
		style = ParagraphStyle('normal')
		p.setFont(style.fontName, style.fontSize)

		# Dibujar la Licencia
		p.drawString(1.3*cm, 28.7*cm,"LICENCIA Na 2011-SL10033")

		# Dibujar RUT
		p.drawString(1.3*cm, 26.3*cm,"RUC: 18297")

		# Dibujar nombre del Cliente
		p.drawString(2.8*cm, 25.4*cm, cliente.nombre)

		# Dibujar Direccion Cliente
		p.drawString(3.7*cm, 24.7*cm, cliente.direccion)

		# Dibujar Rif Cliente
		p.drawString(2.6*cm, 23.9*cm, cliente.rif)

		# Dibujar Telefono Cliente
		p.drawString(7.4*cm, 23.9*cm, cliente.telefono)

		# Dibujar Fecha Factura dia
		fecha = factura.fecha.strftime('%Y-%m-%d %H:%M:%S')
		p.drawString(17.7*cm, 23.9*cm, fecha.split(" ")[0].split("-")[2])
		
		# Dibujar Fecha Factura Mes
		p.drawString(18.6*cm, 23.9*cm, fecha.split(" ")[0].split("-")[1])

		# Dibujar Fecha Factura Dia
		p.drawString(19.3*cm, 23.9*cm, fecha.split(" ")[0].split("-")[0])

		# Indice puntero para el bucle while que dibuja la tabla de la factura
		aux = puntero_producto

	 	# Tabla Factura Productos
	 	total = 0
	 	coord_y = 643
	 	
	 	while puntero_producto<aux+global_limit:			
	 		try:
	 			# Dibujar cantidades de produtos
	 			cantidad = str(total_productos[puntero_producto]['cantidad'])
	 			p.drawString(45, coord_y, cantidad)

				# Dibujar Descripcion de produtos
				descripcion = str(total_productos[puntero_producto]['descripcion'])
				talla = str(total_productos[puntero_producto]['talla'])
				p.drawString(78, coord_y, descripcion + ', Tallas: '+talla)
				
				# Dibujar Precion unitario
				precio = str(total_productos[puntero_producto]['precio_unitario'])
				p.drawString(434, coord_y, precio)
				

				# Dibujar Precio Total
				precio = str(total_productos[puntero_producto]['precio_total'])
				p.drawString(505, coord_y, precio)

				precio_unitario = total_productos[puntero_producto]['precio_unitario']
				cantidad = total_productos[puntero_producto]['cantidad']
				ganancia = total_productos[puntero_producto]['ganancia']

				total += (precio_unitario * cantidad)*(1+(ganancia / 100))
				coord_y -= 15
				
	 		except Exception, e:
	 			pass
	 		
	 		puntero_producto += 1
	 	
	 	aux += global_limit

	 	# Dibujar Precio Subtotal
	 	total_str = str(total)
	 	p.drawString(508, 535, total_str)
		
	 	# Dibujar Iva Valor
	 	iva = 12
		iva_str = str(12)
	 	p.drawString(453, 517, iva_str)
		
		# Dibujar iva calculado sobre el subtotal
		sub_total = (12*total)/100
		sub_total_str = str(sub_total)
		p.drawString(508, 513, sub_total_str)

		# Dibujar Total Final
		total_cotizacion = total + sub_total
		total_cotizacion_str = str(total_cotizacion)
		p.drawString(508, 493, total_cotizacion_str)

		
		p.showPage()
		p.save()
		
		count += 1
		
	# Close the PDF object cleanly, and we're done.
	#p.showPage()
	#p.save()
	return response

def generate_pdf_cotizacion(request,id_cotizacion):
	
	# Declaracion de variables
	iva = 12
	path = './sistema_sfc/static/images/'
	total = 0
	elements = []
	total_productos = []
	objeto = {"cantidad":0, "descripcion":0, "talla":0, "precio_unitario":0, "precio_total":0}

	# Declaracion variables del apartado 'Observaciones' de la cotizacion
	tiempo_entrega = 15
	periodo_validez = 2
	condicion_pago_final = 50
	condicion_pago_inicial = 50
	
	# convertir a formato string para ser dibujado en la cotizacion
	tiempo_entrega_str = str(tiempo_entrega)
	periodo_validez_str = str(periodo_validez)
	condicion_pago_final_str = str(condicion_pago_final)
	condicion_pago_inicial_str = str(condicion_pago_inicial)	

	# Informacion de la cotizacion con id = id_cotizacion
	cotizacion = Cotizacion.objects.get(id = id_cotizacion)
	
	# Productos pertenecientes a la cotizacion con id = id_cotizacion
	productos_cotizacion = Producto_has_cotizacion.objects.filter(cotizacion_id_cotizacion_id = cotizacion.id).extra(select={'cotizacion_id_cotizacion_id':cotizacion.id})
	
	# Todos los productos
	productos = Producto.objects.order_by('id')
	
	# Cliente perteneciente a la cotizacion con id = id_cotizacion
	cliente = Cliente.objects.get(id=cotizacion.cliente_identificacion_id)

	# Observaciones pertenecientes a la cotizacion con id = id_cotizacion
	observaciones_cotizacion = Observacion.objects.filter(cotizacion_id = cotizacion.id).extra(select={'cotizacion_id':cotizacion.id})
	
	
	# Ciclo para obtener todos los productos con su cantidad, talla y precio para ser dibujado en
	# la tabla, el resultado se almacena en el array 'total_productos' de objetos con el formato:
	# {"cantidad":0, "descripcion":0, "talla":0, "precio_unitario":0, "precio_total":0}
	# y el subtotal (suma de todo los precios) en la variable total.

	for item in productos_cotizacion:
		for producto in productos:
			if producto.id == item.producto_id_producto_id:
				objeto['descripcion'] = producto.descripcion
				break
		objeto['cantidad'] = item.cantidad
		objeto['talla'] = item.talla
		objeto['precio_unitario'] = item.precio
		objeto['precio_total'] = (item.precio * item.cantidad)*(1+(item.ganancia / 100))
		total_productos.append(objeto)
		total += (item.precio * item.cantidad)*(1+(item.ganancia / 100))
		objeto = {"cantidad":0, "descripcion":0, "talla":0, "precio_unitario":0, "precio_total":0}

	# Calculo de subtotal, iva, total
	sub_total = total
	iva_total = (total * iva) / 100
	total = iva_total + sub_total

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="COTIZACION '+id_cotizacion+' '+cliente.nombre+'.pdf"'


	# Creacion del pdf 
	# Creacion de la hoja de pdf
	styles = getSampleStyleSheet()
	doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
	
	# Logo de la Empresa
	name_logo = path + "logo.png"
	imagen = Image(name_logo, width=240, height=93)
	imagen.hAlign = 'LEFT'
	elements.append(imagen)
	
	# annadir espacio derecho en la hoja pdf
	elements.append(Spacer(0, -90))

	# icono de telefono
	name_icon_telefono = path + "icon-phone.jpg"
	com_telefono = 'canvas.drawImage("'+name_icon_telefono+'",320,-20,12,12)'
	elements.append(flowables.Macro(com_telefono))
	
	# annadir espacio derecho en la hoja pdf
	elements.append(Spacer(0, 8))
	
	# Agregar estilo al texto del telefono
	ps = ParagraphStyle("indented")
	ps.leftIndent = 340
	texto_telefono = Paragraph('0414-863.67.29 / 0424-919.89.92', ps)
	elements.append(texto_telefono)

	# icono de twitter
	name_icon_twitter = path + "icon-twitter.jpg"
	com_twitter = 'canvas.drawImage("'+name_icon_twitter+'",320,-20,12,12)'
	elements.append(flowables.Macro(com_twitter))
	
	# annadir espacio derecho en la hoja pdf
	elements.append(Spacer(0, 8))
	
	# Agregar estilo al texto
	ps = ParagraphStyle("indented")
	ps.leftIndent = 340
	texto_twitter = Paragraph('diseña2guayana', ps)
	elements.append(texto_twitter)

	# icono de facebook
	name_icon_facebook = path + "icon-facebook.jpg"
	com_facebook = 'canvas.drawImage("'+name_icon_facebook+'",320,-20,12,12)'
	elements.append(flowables.Macro(com_facebook))
	
	# annadir espacio derecho en la hoja pdf
	elements.append(Spacer(0, 8))
	
	# Agregar estilo al texto
	ps = ParagraphStyle("indented")
	ps.leftIndent = 340
	texto_facebook = Paragraph('diseña2guayana', ps)
	elements.append(texto_facebook)

	# icono de correo gmail
	name_icon_gmail = path + "icon-gmail.jpg"
	com_gmail = 'canvas.drawImage("'+name_icon_gmail+'",320,-20,12,12)'
	elements.append(flowables.Macro(com_gmail))
	
	# annadir espacio derecho en la hoja pdf
	elements.append(Spacer(0, 8))
	
	# Agregar estilo al texto
	ps = ParagraphStyle("indented")
	ps.leftIndent = 340
	texto_gmail = Paragraph('diseña2guayana@gmail.com', ps)
	elements.append(texto_gmail)

	# icono de la web
	name_icon_web = path + "icon-web.jpg"
	com_web = 'canvas.drawImage("'+name_icon_web+'",320,-20,12,12)'
	elements.append(flowables.Macro(com_web))
	
	# annadir espacio derecho en la hoja pdf
	elements.append(Spacer(0, 8))
	
	# Agregar estilo al texto
	ps = ParagraphStyle("indented")
	ps.leftIndent = 340
	texto_web = Paragraph('www.diseña2guayana.com', ps)
	elements.append(texto_web)

	# Espacio y estilo del texto nombre de la empresa
	elements.append(Spacer(0, 15))
	ps = ParagraphStyle("indented")
	ps.leftIndent = 70
	texto  = Paragraph('DISEÑA2 GUAYANA, C.A.', ps)
	elements.append(texto )

	# Espacio y estilo del texto rif de la empresa
	ps = ParagraphStyle("indented")
	ps.leftIndent = 85
	texto  = Paragraph('RIF: J-31706245-0', ps)
	elements.append(texto )

	# Espacio y estilo de la oferta y garantia
	elements.append(Spacer(0, -25))
	ps = ParagraphStyle(
        'normal',leftIndent=320, textColor= "blue", fontName='Helvetica-Bold',)
	
	texto  = Paragraph('Envíos y entregas gratis a nivel regional!', ps)
	elements.append(texto )

	ps = ParagraphStyle(
        'normal',leftIndent=380, textColor= "blue", fontName='Helvetica-Bold',)
	texto  = Paragraph('Garantía 100% ', ps)
	elements.append(texto )

	# annadir espacio derecho en la hoja pdf
	elements.append(Spacer(0, 10))
	
	# Parrafos para la informacion del cliente
	ps = ParagraphStyle(
        'normal',textColor= "black", fontName='Helvetica-Bold')
	P0 = Paragraph('Cliente:   '+cliente.nombre, ps)
	P1 = Paragraph('Fecha:   '+str(cotizacion.fecha).split(' ')[0],ps)
	P2 = Paragraph('Rif:   '+str(cliente.rif), ps)
	P3 = Paragraph('Cotización:   '+str(cotizacion.id), ps)
	P4 = Paragraph('Teléfono:   '+str(cliente.telefono), ps)
	P5 = Paragraph('Correo:   '+str(cliente.correo), ps)

	# Tabla con la infrmacion del cliente
	data= [[P0, P1], [P2,P3], [P4,P5]]
	t=Table(data,colWidths=[310, 220], style=[
                    ('BOX',(0,0),(-1,-1),0,colors.black),
                    ('GRID',(0,0),(-1,-1),0.5,colors.black)])
	
	# Alineacion y agregar tabla a la hoja pdf
	t.hAlign = 'LEFT'
	elements.append(t)

	# tabla con le texto informativo
	data= [['Tenemos el agrado de cotizarle los siguientes productos y o servicios']]
	t=Table(data,colWidths=[530], rowHeights=[30], style=[
                    ('BOX',(0,0),(-0,-0),0,colors.black),
                    ('GRID',(0,0),(-0,-0),0.5,colors.black),

                    ('VALIGN',(0,0),(-1,-1),'MIDDLE')])
	
	# Alineacion y agregar tabla a la hoja pdf
	t.hAlign = 'LEFT'
	elements.append(t)

	# Estilos y arreglo para el ****Header***** de la Tabla
	ps = ParagraphStyle(
        'normal',textColor= "black", fontName='Helvetica-Bold', alignment=TA_CENTER,)
	P0 = Paragraph('Item', ps)
	P1 = Paragraph('Descripción', ps)
	P2 = Paragraph('Cantidad', ps)
	P3 = Paragraph('Precio', ps)
	P4 = Paragraph('Monto', ps)

	data= [[P0, P1, P2, P3, P4]]
	
	# estlo para el contenido de la tabla
	centered = ParagraphStyle(name="centered", alignment=TA_CENTER)

    # tabla para agregar los productos y contador para dibujar el numero de productos   
	table = []
	item = 1
	
	# ciclo para dibujar los productos con su estilo en pdf
	for producto in total_productos:
		item1 = Paragraph(str(item), centered)
		item2 = Paragraph(str(producto['descripcion'])+'; Tallas: '+str(producto['talla']), centered)
		item3 = Paragraph(str(producto['cantidad']), centered)
		item4 = Paragraph(str(producto['precio_unitario']), centered)
		item5 = Paragraph(str(producto['precio_total']), centered)
		
		table.append([item1,item2,item3,item4,item5])
		item +=1
	
	#  Estilo y texto de 'SUB-TOTAL' | 'IVA 12%' | 'TOTAL'
	ps = ParagraphStyle('normal',textColor= "black",fontName='Helvetica-Bold', alignment=TA_RIGHT,)
	sub_total_text = Paragraph('SUB-TOTAL',ps)
	iva_text = Paragraph('IVA 12%',ps)
	total_text = Paragraph('TOTAL',ps)

	# Fila para el subtotal, iva y total
	table_row1 = ['',sub_total_text,'','',sub_total]
	table_row2 = ['',iva_text,'','',iva_total]
	table_row3 = ['',total_text,'','',total]
	
	# Agregar a Tabla momentanea de productos
	table.append(table_row1)
	table.append(table_row2)
	table.append(table_row3)
	
	# agregar a tabla final
	for item in table:
		data.append(item)
	
	# Crear la tabla formato para dibujar en PDF

	t2=Table(data, colWidths=[60, 200, 90, 90, 90], style=[
                    ('BOX',(0,0),(-1,-1),0,colors.black),
                    ('GRID',(0,0),(-1,-1),0.5,colors.black),             
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE')])
	t2.hAlign = 'LEFT'
	elements.append(t2)

	elements.append(Spacer(0, 20))
	
	# Estilos para el apartado de Observaciones del pdf
	ps = ParagraphStyle(
        'normal',textColor= "black")
	ps0 = ParagraphStyle(
        'normal',textColor= "black",fontName='Helvetica-Bold', alignment=TA_CENTER,)
	ps1 = ParagraphStyle(
        'normal',fontName='Helvetica-Bold',textColor= "black")
	ps2 = ParagraphStyle(
        'normal',fontName='Helvetica-Bold',textColor= "red")

	P0 = Paragraph('OBSERVACIONES', ps0)
	data = [[P0]]
	for item in observaciones_cotizacion:
		P1 = Paragraph('* '+ item.descripcion, ps)
		data.append([P1])

	'''P0 = Paragraph("* El trabajo se iniciará una vez recibido el pago del  50% de anticipo y la orden de compra correspondiente", ps)
	P1 = Paragraph('* Condición de Pago: '+condicion_pago_inicial_str+' con la  aprobación del presupuesto y '+condicion_pago_final_str+' a la entrega del pedido', ps1)
	P2 = Paragraph('* Los precios unitario no incluyen Iva', ps)
	P3 = Paragraph('* Los precios anexos son en base a esa cantidad solicitada, para otro monto debe consultar', ps)
	P4 = Paragraph('* Los precios y disponibilidad están sujetos a cambios', ps2)
	P5 = Paragraph('* Tiempo de entrega: '+tiempo_entrega_str+' días hábiles', ps)
	P6 = Paragraph('* Validez de la Cotización: '+periodo_validez_str+' días', ps)'''

	# Tabla con las observaciones del PDf
	# data= [[P7],[P0],[P1], [P2] , [P3], [P4], [P5], [P6]]

	t1=Table(data,colWidths=[520], style=[
                    ('BOX',(0,0),(-1,-1),0,colors.black),
                    ('GRID',(0,0),(-1,-1),0.5,colors.black),             
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN',(0,0),(-1,-1),'MIDDLE')])
	
	t1.hAlign = 'LEFT'
	t1.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.green)]))
	t2 = KeepTogether(t1)
	elements.append(t2)
	#elements.append(t1)

	
	# Estilos y parrafos con las firmas del cliente y de la empresa
	ps = ParagraphStyle(
        'normal',textColor= "black",leftIndent=80)
	firma_cliente = Paragraph(cliente.nombre, ps)

	ps = ParagraphStyle(
        'normal',textColor= "black", leftIndent=340)
	firma_disena2Guayana = Paragraph('Diseña2 Guayana, C.A.', ps)

	elements.append(Spacer(0, 50))
	elements.append(firma_cliente)
	elements.append(Spacer(0, -11))
	elements.append(firma_disena2Guayana)

	elements.append(Spacer(0, 50))
	
	# Construir el PDF
	doc.build(elements)
	#doc.build(elements, canvasmaker=NumberedCanvas)
	
	return response