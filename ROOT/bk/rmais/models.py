# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Categoria(models.Model):
	nome_da_categoria = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, verbose_name=u'Url Amigável')
	ativo = models.BooleanField(default=1)
	ordem = models.IntegerField(default=0)
	logo = models.FileField(upload_to='static/uploads/categoria/', null=True, blank=True)
	banner = models.FileField(upload_to='static/uploads/categoria/img-banner', null=True, blank=True)

	
	def __unicode__(self):
		return self.nome_da_categoria

	pass

class Estado(models.Model):
	sigla = models.CharField(max_length=2, null=True, blank=True)
	nome = models.CharField(max_length=72, null=True, blank=True)
	
	def __unicode__(self):
		return self.nome

class Cidade(models.Model):
	estado = models.ForeignKey(Estado)
	nome = models.CharField(max_length=72, null=True, blank=True)
	cep = models.CharField(max_length=8, null=True, blank=True)
	
	def __unicode__(self):
		return self.nome



class Empresa(models.Model):
	# estado = models.ForeignKey(Estado, null=True, blank=True)
	# cidade = models.ForeignKey(Cidade, null=True, blank=True)
	nome_da_empresa = models.CharField(max_length=300)
	endereco = models.CharField(max_length=400)
	nome_do_contato = models.CharField(max_length=150)
	email_do_contato = models.CharField(max_length=200)
	types = (
		(0, 'Leitor'),
		(1, 'Admin'),
		)
	tipo_de_usuario = models.IntegerField(choices=types, default=1, blank=False)
	ativo = models.BooleanField(default=1)

	def __unicode__(self):
		return self.nome_da_empresa

# class Empresa(models.Model):
# 	estado = models.ForeignKey(Estado)
# 	cidade = models.ForeignKey(Cidade)
# 	nome_da_empresa = models.CharField(max_length=300)
# 	endereco = models.CharField(max_length=400)
# 	nome_do_contato = models.CharField(max_length=150)
# 	email_do_contato = models.CharField(max_length=200)
# 	tipo_de_usuario = models.CharField(max_length=100)
# 	ativo = models.BooleanField(default=1)

# 	def __unicode__(self):
# 		return self.nome_da_empresa

class Usuario(models.Model):
	empresa = models.ForeignKey(Empresa, null=True, blank=True)
	nome_do_usuario = models.CharField(max_length=300, null=True, blank=True)
	cidade_de_preferencia = models.ForeignKey(Cidade, null=True, blank=True)
	email = models.CharField(max_length=300, null=True, blank=True)
	senha = models.CharField(max_length=10, null=True, blank=True)
	# ativo = models.BooleanField(default=1)
	options = (
		(0, 'Inativo'),
		(1, 'Ativo'),
		(2, 'Temporario'),
		)
	status = models.IntegerField(choices=options, default=1, blank=False)
	temp_day = (
		(0, '------'),
		(1, '7 Dias'),
		(2, '15 Dias'),
		(3, '30 Dias'),
		(4, '90 Dias'),
	)
	dias_liberado = models.IntegerField(choices=temp_day, default=0, blank=True)
	
	def __unicode__(self):
		return unicode(self.nome_do_usuario)

class Noticia(models.Model):
	categoria = models.ForeignKey(Categoria, null=True, blank=True)
	empresa = models.ManyToManyField(Empresa, null=False, blank=False)
	titulo = models.CharField(max_length=300)
	slug = models.SlugField(max_length=300)
	chamada = models.CharField(max_length=300, null=True, blank=True)
	texto = models.TextField()
	embed_do_video = models.CharField(max_length=300, null=True, blank=True)
	imagem_principal = models.FileField(upload_to='static/uploads/noticia/', null=True, blank=True)
	fonte = models.CharField(max_length=300, null=True, blank=True)
	link_fonte = models.CharField(max_length=300, null=True, blank=True)
	data_de_publicacao = models.DateTimeField('Data de Publicacao', null=True, blank=True)
	data_da_noticia = models.DateField('Data da Noticia', null=True, blank=True)
	ativo = models.BooleanField(default=1)
	data_criacao = models.DateTimeField(auto_now_add=True, blank=True)
	options = (
		(0, ''),
		(1, 'Alarmante'),
		(2, 'Normal'),
		(3, 'Atenção'),
	)
	status = models.IntegerField(choices=options, default=0)

	def __unicode__(self):
		return self.titulo

	class Meta(object):
		ordering = ['-data_da_noticia', '-data_criacao']

class GaleriaImagen(models.Model):
	noticia = models.ForeignKey(Noticia)
	foto = models.FileField(upload_to='static/uploads/galeria-de-imagens/', null=True, blank=True)
	legenda = models.CharField(max_length=300, null=True, blank=True)
	ativo = models.BooleanField(default=1)
	
	def __unicode__(self):
		return self.legenda

class Represa(models.Model):
	nome_da_represa = models.CharField(max_length=200)
	cidade_de_abastecimento = models.ForeignKey(Cidade)
	ativo = models.BooleanField(default=1)

	def __unicode__(self):
		return self.nome_da_represa

class NivelDaAgua(models.Model):
	cidade_de_abastecimento = models.ForeignKey(Represa)
	nivel_da_agua = models.CharField(max_length=3)
	data_criacao = models.DateTimeField('Data de Criacao')
	ativo = models.BooleanField(default=1)


	def __unicode__(self):
		return self.nivel_da_agua

class Pagina(models.Model):
	titulo = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, verbose_name=u'Url Amigável', unique=True)
	chamada = models.CharField(max_length=300, blank=True)
	texto = models.TextField()
	banner = models.FileField(upload_to='static/uploads/pagina/banner/', null=True, blank=True)
	logo = models.FileField(upload_to='static/uploads/pagina/logo/', null=True, blank=True)
	imagem_txt = models.FileField(upload_to='static/uploads/pagina/img-txt/', null=True, blank=True)
	ativo = models.BooleanField(default=1)
	aparecer_no_menu = models.BooleanField(default=0)
	ordem = models.IntegerField(default=0)
	data_criacao = models.DateTimeField(auto_now_add=True, blank=True)


	def __unicode__(self):
		return self.titulo

class Leitura(models.Model):
	usuario = models.ForeignKey(Usuario)
	noticia = models.ForeignKey(Noticia)
	#campo_teste = models.CharField(max_length=10, null=True, blank=True)
	data_de_leitura = models.DateTimeField(auto_now_add=True, blank=True, null=True)


	def __unicode__(self):
		# return "Lida em %s por %s" % (self.data_de_leitura, self.usuario.nome_do_usuario)
		return "%s" % self.usuario.id

	def noticia_lida(self):
		return "%s" % self.noticia.id