# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0009_auto_20150305_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='senha',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
