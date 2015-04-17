from django import template
from django.template import Library
from datetime import date
import datetime
from ROOT.rmais.models import Categoria, Noticia

register = template.Library()

@register.filter 
def date_add_days(value, arg):
	# print "Value: %s" % value
	return value + datetime.timedelta(days = arg)

@register.filter 
def qtde_de_dias(data_criacao, tempo_acesso):
	data_expiracao = data_criacao

	if tempo_acesso == 1:
		data_expiracao = data_criacao + datetime.timedelta(days = 7)

	elif tempo_acesso == 2:
		data_expiracao = data_criacao + datetime.timedelta(days = 15)

	elif tempo_acesso == 3:
		data_expiracao = data_criacao + datetime.timedelta(days = 30)

	elif tempo_acesso == 4:
		data_expiracao = data_criacao + datetime.timedelta(days = 90)

	return data_expiracao