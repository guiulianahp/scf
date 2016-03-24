# -*- coding: utf-8 -*-
import json
from io import BytesIO
from itertools import chain
from django.contrib import auth
from django.utils import translation
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles.templatetags.staticfiles import static
from sistema_sfc.apps.scf.models import Cliente, Producto, Cotizacion, Factura, Prospecto, Producto_has_cotizacion, Observacion_por_defecto



@login_required(login_url='/login/')
def index_view(request):
	resultado = Producto.objects.order_by('id')
	
	return render_to_response('home/index.html',{'resultado' : resultado}, context_instance=RequestContext(request))


def login_user(request):
    logout(request)
    username = password = ''
    mensaje = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        mensaje = 'Nombre de usuario o contraseña no válido'
    return render_to_response('home/login.html', {'mensaje': mensaje}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return render_to_response('home/login.html', context_instance=RequestContext(request))

@ensure_csrf_cookie
def cliente_view(request):
	if request.method=="POST":

		if "input_id" in request.POST:
			try:
				id_producto = request.POST['input_id']
				p = Cliente.objects.get(id=id_producto)
				
				
				try:
				    cotizacion = Cotizacion.objects.get(cliente_identificacion_id=p.id)
				    boolean = True
				except Cotizacion.DoesNotExist:
				    boolean = False
				    
				if boolean:
					print 'aqui'
					mensaje = {"status":"False", "mensaje":"El Cliente posee cotizaciones activas",
					"input_id":p.id}
					
				else:
					mensaje = {"status":"True","input_id":p.id}
					p.delete() # Elinamos objeto de la base de datos
				return HttpResponse(json.dumps(mensaje),content_type='application/json')
			except Exception as e:
				print e
				id_producto = request.POST['input_id']
				p = Cliente.objects.get(id=id_producto)
				mensaje = {"status":"False","input_id":p.id}
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

	resultado = Cliente.objects.order_by('rif')
	return render_to_response('home/cliente.html', {'resultado' : resultado}, context_instance=RequestContext(request))

@ensure_csrf_cookie
def producto_view(request):
	if request.method=="POST":

		if "input_id" in request.POST:
			try:
				id_producto = request.POST['input_id']
				p = Producto.objects.get(id=id_producto)
				mensaje = {"status":"True","input_id":p.id}
				p.delete() # Elinamos objeto de la base de datos
				return HttpResponse(json.dumps(mensaje),content_type='application/json')
			except:
				id_producto = request.POST['input_id']
				p = Producto.objects.get(id=id_producto)
				mensaje = {"status":"False","input_id":p.id}
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

	resultado = Producto.objects.order_by('id')
	return render_to_response('home/producto.html', {'resultado' : resultado}, context_instance=RequestContext(request))

@ensure_csrf_cookie
def cotizacion_view(request):
	# Variables:
	resultado = []
	objeto = {'id':'','fecha':'', 'nombre':'', 'editable':''}

	# Si selecciona opcion de eliminar cotizacion
	if request.method=="POST":

		if "input_id" in request.POST:
			try:
				id_producto = request.POST['input_id']
				p = Cotizacion.objects.get(id=id_producto)
				mensaje = {"status":"True","input_id":p.id}
				Producto_has_cotizacion.objects.filter(cotizacion_id_cotizacion=id_producto).delete()
				p.delete() # Elinamos objeto de la base de datos
				return HttpResponse(json.dumps(mensaje),content_type='application/json')
			except:
				id_producto = request.POST['input_id']
				p = Cotizacion.objects.get(id=id_producto)
				mensaje = {"status":"False","input_id":p.id}
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

	# Listado de cotizaciones
	cotizaciones = Cotizacion.objects.order_by('id')
	
	# Listado de clientes
	clientes = Cliente.objects.order_by('id')
	
	# Listado de facturas
	facturas = Factura.objects.order_by('id')

	# ciclo para ordenar las cotizacion con id | fecha y nombre de cliente
	# ademas se colocara la opcion disabled para poder validar si la cotizacion
	# puede ser editada (habilitacion o deshabilitacion del boton editar)
	
	
    

	for cotizacion in cotizaciones:
		id_client = cotizacion.cliente_identificacion_id
		for cliente in clientes:
			if id_client == cliente.id:
				objeto['id'] = cotizacion.id
				objeto['fecha'] = cotizacion.fecha
				objeto['nombre'] = cliente.nombre
				
				for factura in facturas:
					if factura.cotizacion_id_cotizacion_id == cotizacion.id:
						objeto['editable'] = 'disabled'

				resultado.append(objeto)
				objeto = {'id':'','fecha':'', 'nombre':'', 'editable':''}
				break

	return render_to_response('home/cotizacion.html', {'resultado' : resultado}, context_instance=RequestContext(request))

@ensure_csrf_cookie
def facturacion_view(request):
	if request.method=="POST":

		if "input_id" in request.POST:
			try:
				id_producto = request.POST['input_id']
				p = Factura.objects.get(id=id_producto)

				cotizacion = Cotizacion.objects.get(id=p.cotizacion_id_cotizacion_id)
				cotizacion.estado = 0
				cotizacion.save()
				mensaje = {"dialogo":"Factura Eliminada Correctamente", "status":"True","input_id":p.id}
				p.delete() # Elinamos objeto de la base de datos
				return HttpResponse(json.dumps(mensaje),content_type='application/json')
			except:
				id_producto = request.POST['input_id']
				p = Factura.objects.get(id=id_producto)
				mensaje = {"dialogo":"Error al eliminar factura","status":"False","input_id":p.id}
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

	resultado = []
	facturas = Factura.objects.order_by('id')
	cotizaciones = Cotizacion.objects.order_by('id')
	clientes = Cliente.objects.order_by('id')
	objeto = {'id':'', 'num_factura':'', 'fecha':'','id_cotizacion':'','cliente':''}

	for factura in facturas:
		id_cotizacion = factura.cotizacion_id_cotizacion_id
		for cotizacion in cotizaciones:
			if id_cotizacion == cotizacion.id:
				id_cliente = cotizacion.cliente_identificacion_id
				for cliente in clientes:
					if id_cliente == cliente.id:
						nombre = cliente.nombre
						objeto['id'] = factura.id
						objeto['num_factura'] = factura.num_factura
						objeto['fecha'] = factura.fecha
						objeto['id_cotizacion'] = id_cotizacion
						objeto['cliente'] = nombre
						resultado.append(objeto)
						objeto = {'id':'', 'num_factura':'', 'fecha':'','id_cotizacion':'','cliente':''}

	return render_to_response('home/facturacion.html', {'resultado' : resultado}, context_instance=RequestContext(request))

@ensure_csrf_cookie
def prospecto_view(request):
	if request.method=="POST":
		if "input_id" in request.POST:
			try:
				id_producto = request.POST['input_id']
				p = Prospecto.objects.get(id=id_producto)
				mensaje = {"status":"True","input_id":p.id}
				p.delete() # Elinamos objeto de la base de datos
				return HttpResponse(json.dumps(mensaje),content_type='application/json')
			except:
				id_producto = request.POST['input_id']
				p = Prospecto.objects.get(id=id_producto)
				mensaje = {"status":"False","input_id":p.id}
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

		if "input_id_prospecto" in request.POST:
			try:
				id_prospecto = request.POST['input_id_prospecto']
				p = Prospecto.objects.get(id=id_prospecto)

				objeto = {"nombre":p.nombre, "telefono":p.telefono, "correo":p.correo, "id":p.id}
				mensaje = {"status":"True","data":objeto}
				#return render_to_response('scf/convertir_prospecto.html')
				return HttpResponse(json.dumps(mensaje),content_type='application/json')
				#return respuesta
				#p.delete() # Elinamos objeto de la base de datos
				#return render_to_response('scf/convertir_prospecto.html', {'resultado' : p}, context_instance=RequestContext(request))
			except:
				id_prospecto = request.POST['input_id_prospecto']
				p = Prospecto.objects.get(id=id_prospecto)
				objeto = {"nombre":p.nombre, "telefono":p.telefono, "correo":p.correo, "id":p.id}
				mensaje = {"status":"False","data":objeto}
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

	else:
		resultado = Prospecto.objects.order_by('id')
		return render_to_response('home/prospecto.html', {'resultado' : resultado}, context_instance=RequestContext(request))

def observacion_view(request):

	count = 1
	resultado = []
	json_observacion = {"id":"", "num":"", "observacion": ""}
	observacion = Observacion_por_defecto.objects.order_by('id')
	
	
	if request.method=="POST":

		if "input_id" in request.POST:
			try:
				id_observacion = int(request.POST['input_id'])
				p 			   = Observacion_por_defecto.objects.get(id=id_observacion)
				mensaje 	   = {"status":"True","input_id":p.id}
				p.delete() # Elinamos objeto de la base de datos
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

			except Exception as e:
				print e
				id_observacion = request.POST['input_id']
				p 	           = Observacion_por_defecto.objects.get(id=id_observacion)
				mensaje 	   = {"status":"False","input_id":p.id}
				return HttpResponse(json.dumps(mensaje),content_type='application/json')

	for item in observacion:
		json_observacion = {"id": item.id, "num":count, "observacion": item.descripcion}
		resultado.append(json_observacion)
		json_observacion = {"id":"", "num":"", "observacion": ""}
		count += 1

	return render_to_response('home/observacion.html',{'observaciones': resultado}, context_instance=RequestContext(request))