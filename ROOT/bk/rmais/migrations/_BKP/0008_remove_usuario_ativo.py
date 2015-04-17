# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0007_auto_20150305_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='ativo',
        ),
    ]
