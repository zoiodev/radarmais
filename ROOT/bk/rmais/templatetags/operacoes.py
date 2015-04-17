from django import template
from django.template import Library 

register = template.Library()

@register.filter 
def subtract(value, arg):
	print "Value: %s" % value
	return int(value) - int(arg)
