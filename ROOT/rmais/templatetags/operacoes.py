from django import template
from django.template import Library
import time
import datetime

from ROOT.rmais.models import Categoria, Noticia

register = template.Library()

@register.filter 
def subtract(value, arg):
	# print "Value: %s" % value
	return int(value) - int(arg)


@register.filter
def primeira_noticia(categoria, campo):
	noticias = categoria.noticia_set.all()


	# print "CATEGORIA: %s" % categoria
	for noticia in noticias:

		data_campo = noticia.data_de_publicacao.strftime("%d-%m-%Y %H:%M")
		data_agora = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

		# print noticia.titulo
		# print "%s x %s" % (noticia.data_de_publicacao, data_agora)

		if data_campo <= data_agora:
			# print noticia.titulo
			retorno = getattr(noticia, campo)
			# print "- - - - - - - - - - - - - - - - - - "
			break

	# print "- - - - - - - - - - - - - - - - - - "

	# print categoria

	return retorno