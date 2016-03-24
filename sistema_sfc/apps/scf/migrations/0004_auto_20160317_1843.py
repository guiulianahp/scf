# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scf', '0003_observacion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observacion',
            old_name='id_cotizacion',
            new_name='cotizacion',
        ),
    ]
