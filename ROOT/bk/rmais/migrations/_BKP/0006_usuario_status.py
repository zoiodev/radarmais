# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0005_remove_usuario_temporario'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'------'), (1, b'Inativo'), (2, b'Ativo'), (3, b'Temporario')]),
            preserve_default=True,
        ),
    ]
