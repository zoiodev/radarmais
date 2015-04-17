# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0003_remove_usuario_temporario'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='temporario',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
