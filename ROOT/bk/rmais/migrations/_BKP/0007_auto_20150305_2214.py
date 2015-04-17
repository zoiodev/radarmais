# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0006_usuario_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cidade_de_preferencia',
            field=models.ForeignKey(blank=True, to='rmais.Cidade', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='dias_liberado',
            field=models.IntegerField(default=0, blank=True, choices=[(0, b'------'), (1, b'7 Dias'), (2, b'15 Dias'), (3, b'30 Dias'), (4, b'90 Dias')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='empresa',
            field=models.ForeignKey(blank=True, to='rmais.Empresa', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nome_do_usuario',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='senha',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='status',
            field=models.IntegerField(default=1, choices=[(0, b'Inativo'), (1, b'Ativo'), (2, b'Temporario')]),
            preserve_default=True,
        ),
    ]
