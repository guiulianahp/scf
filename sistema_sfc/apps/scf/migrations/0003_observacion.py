# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scf', '0002_auto_20160309_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('id_cotizacion', models.ForeignKey(to='scf.Cotizacion')),
            ],
        ),
    ]
