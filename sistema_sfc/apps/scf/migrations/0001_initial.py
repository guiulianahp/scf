# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rif', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('cliente_identificacion', models.ForeignKey(to='scf.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('cotizacion_id_cotizacion', models.ForeignKey(to='scf.Cotizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200)),
                ('precio_tp', models.FloatField()),
                ('precio_tg', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto_has_cotizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField()),
                ('ganancia', models.FloatField()),
                ('cotizacion_id_cotizacion', models.ForeignKey(to='scf.Cotizacion')),
                ('producto_id_producto', models.ForeignKey(to='scf.Producto')),
            ],
        ),
        migrations.CreateModel(
            name='Prospecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.CharField(max_length=200)),
            ],
        ),
    ]
