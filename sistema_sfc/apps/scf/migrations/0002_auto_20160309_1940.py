# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='factura',
            name='num_factura',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto_has_cotizacion',
            name='precio',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto_has_cotizacion',
            name='talla',
            field=models.CharField(default=b'S', max_length=20),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='rif',
            field=models.CharField(max_length=100),
        ),
    ]
