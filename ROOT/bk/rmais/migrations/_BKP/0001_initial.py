# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome_da_categoria', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, verbose_name='Url Amig\xe1vel')),
                ('ativo', models.BooleanField(default=1)),
                ('ordem', models.IntegerField(default=0)),
                ('logo', models.FileField(null=True, upload_to=b'static/uploads/categoria/', blank=True)),
                ('banner', models.FileField(null=True, upload_to=b'static/uploads/categoria/img-banner', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=72)),
                ('cep', models.CharField(max_length=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome_da_empresa', models.CharField(max_length=300)),
                ('endereco', models.CharField(max_length=400)),
                ('nome_do_contato', models.CharField(max_length=150)),
                ('email_do_contato', models.CharField(max_length=200)),
                ('tipo_de_usuario', models.CharField(max_length=100)),
                ('ativo', models.BooleanField(default=1)),
                ('cidade', models.ForeignKey(to='rmais.Cidade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(max_length=2)),
                ('nome', models.CharField(max_length=72)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GaleriaImagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foto', models.FileField(null=True, upload_to=b'static/uploads/galeria-de-imagens/', blank=True)),
                ('legenda', models.CharField(max_length=300, null=True, blank=True)),
                ('ativo', models.BooleanField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NivelDaAgua',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nivel_da_agua', models.CharField(max_length=3)),
                ('data_criacao', models.DateTimeField(verbose_name=b'Data de Criacao')),
                ('ativo', models.BooleanField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=300)),
                ('slug', models.SlugField(max_length=300)),
                ('chamada', models.CharField(max_length=300, null=True, blank=True)),
                ('texto', models.TextField()),
                ('embed_do_video', models.CharField(max_length=300, null=True, blank=True)),
                ('imagem_principal', models.FileField(null=True, upload_to=b'static/uploads/noticia/', blank=True)),
                ('fonte', models.CharField(max_length=300, null=True, blank=True)),
                ('link_fonte', models.CharField(max_length=300, null=True, blank=True)),
                ('data_de_publicacao', models.DateTimeField(null=True, verbose_name=b'Data de Publicacao', blank=True)),
                ('ativo', models.BooleanField(default=1)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b''), (1, b'Alarmante'), (2, b'Normal'), (3, b'Aten\xc3\xa7\xc3\xa3o')])),
                ('categoria', models.ForeignKey(blank=True, to='rmais.Categoria', null=True)),
                ('empresa', models.ManyToManyField(to='rmais.Empresa')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Url Amig\xe1vel')),
                ('chamada', models.CharField(max_length=300, blank=True)),
                ('texto', models.TextField()),
                ('banner', models.FileField(null=True, upload_to=b'static/uploads/pagina/banner/', blank=True)),
                ('logo', models.FileField(null=True, upload_to=b'static/uploads/pagina/logo/', blank=True)),
                ('imagem_txt', models.FileField(null=True, upload_to=b'static/uploads/pagina/img-txt/', blank=True)),
                ('ativo', models.BooleanField(default=1)),
                ('aparecer_no_menu', models.BooleanField(default=0)),
                ('ordem', models.IntegerField(default=0)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Represa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome_da_represa', models.CharField(max_length=200)),
                ('ativo', models.BooleanField(default=1)),
                ('cidade_de_abastecimento', models.ForeignKey(to='rmais.Cidade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome_do_usuario', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=300)),
                ('senha', models.CharField(max_length=10)),
                ('ativo', models.BooleanField(default=1)),
                ('temporario', models.BooleanField(default=False)),
                ('dias_liberado', models.IntegerField(default=0, choices=[(0, b'------'), (1, b'7 Dias'), (2, b'15 Dias'), (3, b'30 Dias'), (4, b'90 Dias')])),
                ('cidade_de_preferencia', models.ForeignKey(to='rmais.Cidade')),
                ('empresa', models.ForeignKey(to='rmais.Empresa')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='niveldaagua',
            name='cidade_de_abastecimento',
            field=models.ForeignKey(to='rmais.Represa'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='galeriaimagen',
            name='noticia',
            field=models.ForeignKey(to='rmais.Noticia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='empresa',
            name='estado',
            field=models.ForeignKey(to='rmais.Estado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cidade',
            name='estado',
            field=models.ForeignKey(to='rmais.Estado'),
            preserve_default=True,
        ),
    ]
