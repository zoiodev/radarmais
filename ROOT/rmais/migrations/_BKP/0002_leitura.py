# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rmais', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leitura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_de_leitura', models.DateTimeField(auto_now_add=True, null=True)),
                ('noticia', models.ForeignKey(to='rmais.Noticia')),
                ('usuario', models.ForeignKey(to='rmais.Usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
