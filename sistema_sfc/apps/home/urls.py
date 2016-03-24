from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('sistema_sfc.apps.home.views',
url(r'^$','index_view', name = 'index_view'),
url(r'^login/$', 'login_user', name='login'),
url(r'^logout/$', logout, name='logout'),
url(r'^cliente/$', 'cliente_view', name = 'cliente'),
url(r'^producto/$', 'producto_view', name = 'producto'),
url(r'^cotizacion/$', 'cotizacion_view', name = 'cotizacion'),
url(r'^facturacion/$', 'facturacion_view', name = 'facturacion'),
url(r'^prospecto/$', 'prospecto_view', name = 'prospecto'),
url(r'^observacion/$', 'observacion_view', name = 'observacion')

)
