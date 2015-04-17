# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0008_remove_usuario_ativo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='senha',
            field=models.TextField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
