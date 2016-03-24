from django import forms
from models import Cliente, Producto, Factura, Cotizacion, Prospecto
from django.contrib.admin import widgets 


class addClienteForm(forms.Form):
	rif 		= forms.CharField(widget = forms.TextInput())
	nombre 		= forms.CharField(widget = forms.TextInput())
	telefono 	= forms.CharField(widget = forms.TextInput())
	correo 		= forms.CharField(widget = forms.TextInput())
	direccion 	= forms.CharField(widget = forms.TextInput())

	def clean(self):
		return self.cleaned_data

class addProductoForm(forms.Form):
	nombre 		= forms.CharField(widget = forms.TextInput())
	descripcion = forms.CharField(widget = forms.TextInput())
	precio_talla_pequena 	= forms.FloatField(widget = forms.TextInput())
	
	
	def clean(self):
		return self.cleaned_data

class addProspectoForm(forms.Form):
	nombre 		= forms.CharField(widget = forms.TextInput())
	telefono 	= forms.CharField(widget = forms.TextInput())
	correo 		= forms.CharField(widget = forms.TextInput())
	
	def clean(self):
		return self.cleaned_data


class addCotizacion(forms.Form):
	id_cliente	= forms.ModelChoiceField(queryset=Cliente.objects.values_list('nombre', flat=True),empty_label="Elige un Cliente",)
	fecha 		= forms.DateField()

	def clean(self):
		return self.cleaned_data

class addObservacionForm(forms.Form):
	descripcion = forms.CharField(widget = forms.TextInput())

	def clean(self):
		return self.cleaned_data

        