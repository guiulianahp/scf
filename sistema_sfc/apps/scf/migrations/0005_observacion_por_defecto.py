# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scf', '0004_auto_20160317_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observacion_por_defecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
    ]
