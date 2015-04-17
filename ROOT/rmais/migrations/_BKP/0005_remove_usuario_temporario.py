# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0004_usuario_temporario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='temporario',
        ),
    ]
